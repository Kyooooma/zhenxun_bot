import asyncio
import os
from typing import List, Union

from configs.path_config import IMAGE_PATH
from models.group_member_info import GroupInfoUser
from utils.image_utils import BuildMat


async def init_rank(
    title: str,
    all_user_id: List[str],
    all_user_data: List[Union[int, float]],
    group_id: int,
    total_count: int = 10,
) -> BuildMat:
    """
    说明:
        初始化通用的数据排行榜
    参数:
        :param title: 排行榜标题
        :param all_user_id: 所有用户的qq号
        :param all_user_data: 所有用户需要排行的对应数据
        :param group_id: 群号，用于从数据库中获取该用户在此群的昵称
        :param total_count: 获取人数总数
    """
    _uname_lst = []
    _num_lst = []
    for i in range(min(len(all_user_id), total_count)):
        _max = max(all_user_data)
        max_user_id = all_user_id[all_user_data.index(_max)]
        all_user_id.remove(max_user_id)
        all_user_data.remove(_max)
        if user := await GroupInfoUser.get_or_none(
            user_qq=str(max_user_id), group_id=str(group_id)
        ):
            print(user.user_qq, user.user_name, user.group_id)
            user_name = user.user_name
        else:
            user_name = f"{max_user_id}"
            print(user_name)
        _uname_lst.append(user_name)
        _num_lst.append(_max)
    _uname_lst.reverse()
    _num_lst.reverse()
    return _init_rank_graph(title, _uname_lst, _num_lst)


def _init_rank_graph(
    title: str, _uname_lst: List[str], _num_lst: List[Union[int, float]]
) -> BuildMat:
    """
    生成排行榜统计图
    :param title: 排行榜标题
    :param _uname_lst: 用户名列表
    :param _num_lst: 数值列表
    """
    print(_uname_lst)
    print(_num_lst)
    image = BuildMat(
        y=_num_lst,
        y_name="* 可以在命令后添加数字来指定排行人数 至多 50 *",
        mat_type="barh",
        title=title,
        x_index=_uname_lst,
        display_num=True,
        x_rotate=30,
        background=[
            f"{IMAGE_PATH}/background/create_mat/{x}"
            for x in os.listdir(f"{IMAGE_PATH}/background/create_mat")
        ],
        bar_color=["*"],
        font_size=10
    )
    image.gen_graph()
    return image
