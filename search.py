import nltk
import os
from supabase import create_client, Client
from dotenv import load_dotenv

def search(query) -> list[str]:
    load_dotenv()

    url: str = os.environ.get("SUPABASE_URL")
    key: str = os.environ.get("SUPABASE_KEY")
    supabase: Client = create_client(url, key)

    keywords = nltk.WhitespaceTokenizer().tokenize(query.lower())

    final_results = {}

    response = (
        supabase
        .table("sites")
        .select("*", count="exact", head=True)
        .execute()
    )
    sites_count = response.count

    for word in keywords:
        keyword_response = (
            supabase
            .table("keywords")
            .select("*")
            .eq("keyword", word)
            .execute()
        )

        if len(keyword_response.data) == 0:
            continue

        document_frequency = keyword_response.data[0]['document_frequency']
        keyword_id = keyword_response.data[0]['keyword_id']

        postings_response = (
            supabase.table('postings')
            .select("*")
            .eq("keyword_id", keyword_id)
            .execute()
        )

        site_ids = []
        for result in postings_response.data:
            site_ids.append(result['site_id'])

        sites_response = (
            supabase.table('sites')
            .select("*")
            .in_("site_id", site_ids)
            .execute()
        )

        site_data = {}

        for site in sites_response.data:
            site_data[site['site_id']] = site
        
        print(site_data)

        for result in postings_response.data:
            term_count = result['term_frequency']
            site_id = result['site_id']

            site_length = site_data[site_id]['doc_length']
            term_frequency = term_count / site_length

            inverse_document_frequency = sites_count / document_frequency

            url = site_data[site_id]['url']

            if (url in final_results):
                final_results[url] += term_frequency * inverse_document_frequency
            else:
                final_results[url] = term_frequency * inverse_document_frequency
        
    final_results = dict(sorted(final_results.items(), key=lambda item: item[1], reverse=True))
    final_results = list(final_results.items())
    
    return final_results