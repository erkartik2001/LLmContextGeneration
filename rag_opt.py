from vector_db import store_docs_embedding, query_docs
from get_web_content import store_web_data


def generate_context(query):
    try:
        flag = store_web_data(query=query)
        if flag:
            res = store_docs_embedding()

            if not res:
                print("Error storing document in Vector DB")
                return None
            
            context = query_docs(query=query)
            # print("Context Generated--->\n")
            # print(context)
            return context
        
        else:
            return None
        
    except Exception as e:
        print(f"Cannot generate context error {e}")
        return None
    


