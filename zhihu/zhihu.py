from selenium import webdriver
import json
import re


def get_answers(question):
    browser = webdriver.Chrome()  # 使用PhantomJS会出现乱码，不知怎么解决
    offset = 0
    while True:
        item = {}
        # 每次请求20个回答
        url = f'https://www.zhihu.com/api/v4/questions/{question}/answers?include=data%5B%2A%5D.is_normal%2Cadmin_closed_comment%2Creward_info%2Cis_collapsed%2Cannotation_action%2Cannotation_detail%2Ccollapse_reason%2Cis_sticky%2Ccollapsed_by%2Csuggest_edit%2Ccomment_count%2Ccan_comment%2Ccontent%2Ceditable_content%2Cvoteup_count%2Creshipment_settings%2Ccomment_permission%2Ccreated_time%2Cupdated_time%2Creview_info%2Crelevant_info%2Cquestion%2Cexcerpt%2Crelationship.is_authorized%2Cis_author%2Cvoting%2Cis_thanked%2Cis_nothelp%2Cis_labeled%2Cis_recognized%2Cpaid_info%2Cpaid_info_content%3Bdata%5B%2A%5D.mark_infos%5B%2A%5D.url%3Bdata%5B%2A%5D.author.follower_count%2Cbadge%5B%2A%5D.topics&limit=20&offset={offset}&platform=desktop&sort_by=default'
        browser.get(url)
        dict = re.search('<html><head></head><body><pre style="word-wrap: break-word; white-space: pre-wrap;">(.*?)[\s]</pre></body></html>', browser.page_source).group(1)
        datas = json.loads(dict)
        if not datas['data']:
            # datas['data']无数据则爬取结束
            break
        question_info = datas['data'][0]
        # 问题信息
        item['question_id'] = question_info['question']['id']
        item['question_title'] = question_info['question']['title']
        item['question_url'] = question_info['question']['url']
        for data in datas['data']:
            # 回答用户信息
            item['answer_id'] = data['author']['id']
            item['answer_type'] = data['answer_type']
            item['answer_name'] = data['author']['name']
            item['voteup_count'] = data['voteup_count']
            item['comment_count'] = data['comment_count']
            item['answer_url'] = 'https://www.zhihu.com/people/' + data['author']['url_token']
            item['content'] = data['content']

            print(item)

        offset += 20
    browser.close()


if __name__ == '__main__':
    question = 20465493
    get_answers(question)

