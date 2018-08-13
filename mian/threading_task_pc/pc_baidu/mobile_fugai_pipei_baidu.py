
from threading_task_pc import zhongzhuanqi
def Baidu_Zhidao_yuming_mobile(yinqing, keyword, domain, detail_id):
    result = zhongzhuanqi.fugaiChaxun(detail_id, yinqing, keyword, ','.join(domain.split(',')))
    if result:
        return result
