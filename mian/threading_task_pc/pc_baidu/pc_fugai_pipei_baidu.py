
from threading_task_pc import zhongzhuanqi

def Baidu_Zhidao_yuming_pc(yinqing, keyword, domain, detail_id):
    str_order = '0'
    mohu_pipei_list = domain.split(',')
    result = zhongzhuanqi.fugaiChaxun(detail_id, yinqing, keyword, ','.join(mohu_pipei_list))
    if result:
        return result
