

from threading_task_pc import zhongzhuanqi
def Dao_Hang_360_yuming_pc(search_engine, keyword, domain, detail_id):
    mohu_pipei_list = domain.split(',')
    result = zhongzhuanqi.fugaiChaxun(detail_id, search_engine, keyword, ','.join(mohu_pipei_list))
    if result:
        return result


