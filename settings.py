# 输入根路径 国学大师
ROOT_DIR_GXDS: str = 'input/guoxuedashi'

# 输入根路径 八斗文学
ROOT_DIR_BD: str = 'input/8dou'

# 输出路径
ROOT_OUTPUT: str = 'output/'

# 阈值 content 余弦相似度阈值
THRESHOLD_COS: float = 0.9

# 作为初筛的正文子串长度
FILTER_LEN: int = 4

# 是否输出 summary
# 默认在 output 目录下
OUTPUT_SUMMARY: bool = True

# 是否输出 cos value 统计
OUTPUT_COS: bool = True
