from sqlalchemy import create_engine, Column, Integer, String, Float, Date, Time, ForeignKey, Boolean
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

Base = declarative_base()

class Type(Base):
    __tablename__ = 'types'

    id = Column(Integer, primary_key=True, autoincrement=True)
    type = Column(String, unique=True, nullable=False)

class Movie(Base):
    __tablename__ = 'movies'

    # 基本資訊
    # movie_id = Column(Integer, primary_key=True, autoincrement=True)
    imdb_id = Column(String, primary_key=True)
    title = Column(String, nullable=False)
    type_id = Column(Integer, ForeignKey('types.id'))
    release_year = Column(Integer)
    imdb_average_rating = Column(Float)
    imdb_num_votes = Column(Integer)
    
    # 電影類型 (Boolean)
    action = Column(Boolean, default=False)
    adult = Column(Boolean, default=False)
    adventure = Column(Boolean, default=False)
    animation = Column(Boolean, default=False)
    biography = Column(Boolean, default=False)
    comedy = Column(Boolean, default=False)
    crime = Column(Boolean, default=False)
    documentary = Column(Boolean, default=False)
    drama = Column(Boolean, default=False)
    family = Column(Boolean, default=False)
    fantasy = Column(Boolean, default=False)
    film_noir = Column(Boolean, default=False)
    game_show = Column(Boolean, default=False)
    history = Column(Boolean, default=False)
    horror = Column(Boolean, default=False)
    music = Column(Boolean, default=False)
    musical = Column(Boolean, default=False)
    mystery = Column(Boolean, default=False)
    news = Column(Boolean, default=False)
    reality_tv = Column(Boolean, default=False)
    romance = Column(Boolean, default=False)
    sci_fi = Column(Boolean, default=False)
    short = Column(Boolean, default=False)
    sport = Column(Boolean, default=False)
    talk_show = Column(Boolean, default=False)
    thriller = Column(Boolean, default=False)
    war = Column(Boolean, default=False)
    western = Column(Boolean, default=False)

    # 國家代碼 (Boolean)
    ad = Column(Boolean, default=False)  # 安道爾
    ae = Column(Boolean, default=False)  # 阿拉伯聯合大公國
    ag = Column(Boolean, default=False)  # 安地卡及巴布達
    al = Column(Boolean, default=False)  # 阿爾巴尼亞
    ao = Column(Boolean, default=False)  # 安哥拉
    ar = Column(Boolean, default=False)  # 阿根廷
    at = Column(Boolean, default=False)  # 奧地利
    au = Column(Boolean, default=False)  # 澳洲
    az = Column(Boolean, default=False)  # 亞塞拜然
    ba = Column(Boolean, default=False)  # 波士尼亞與赫塞哥維納
    bb = Column(Boolean, default=False)  # 巴貝多
    be = Column(Boolean, default=False)  # 比利時
    bg = Column(Boolean, default=False)  # 保加利亞
    bh = Column(Boolean, default=False)  # 巴林
    bm = Column(Boolean, default=False)  # 百慕達
    bo = Column(Boolean, default=False)  # 玻利維亞
    br = Column(Boolean, default=False)  # 巴西
    bs = Column(Boolean, default=False)  # 巴哈馬
    by = Column(Boolean, default=False)  # 白俄羅斯
    bz = Column(Boolean, default=False)  # 貝里斯
    ca = Column(Boolean, default=False)  # 加拿大
    ch = Column(Boolean, default=False)  # 瑞士
    ci = Column(Boolean, default=False)  # 象牙海岸
    cl = Column(Boolean, default=False)  # 智利
    cm = Column(Boolean, default=False)  # 喀麥隆
    co = Column(Boolean, default=False)  # 哥倫比亞
    cr = Column(Boolean, default=False)  # 哥斯大黎加
    cu = Column(Boolean, default=False)  # 古巴
    cv = Column(Boolean, default=False)  # 維德角
    cy = Column(Boolean, default=False)  # 賽普勒斯
    cz = Column(Boolean, default=False)  # 捷克
    de = Column(Boolean, default=False)  # 德國
    dk = Column(Boolean, default=False)  # 丹麥
    do = Column(Boolean, default=False)  # 多明尼加
    dz = Column(Boolean, default=False)  # 阿爾及利亞
    ec = Column(Boolean, default=False)  # 厄瓜多
    ee = Column(Boolean, default=False)  # 愛沙尼亞
    eg = Column(Boolean, default=False)  # 埃及
    es = Column(Boolean, default=False)  # 西班牙
    fi = Column(Boolean, default=False)  # 芬蘭
    fj = Column(Boolean, default=False)  # 斐濟
    fr = Column(Boolean, default=False)  # 法國
    gb = Column(Boolean, default=False)  # 英國
    gf = Column(Boolean, default=False)  # 法屬圭亞那
    gg = Column(Boolean, default=False)  # 根西島
    gh = Column(Boolean, default=False)  # 迦納
    gi = Column(Boolean, default=False)  # 直布羅陀
    gq = Column(Boolean, default=False)  # 赤道幾內亞
    gr = Column(Boolean, default=False)  # 希臘
    gt = Column(Boolean, default=False)  # 瓜地馬拉
    hk = Column(Boolean, default=False)  # 香港
    hn = Column(Boolean, default=False)  # 宏都拉斯
    hr = Column(Boolean, default=False)  # 克羅埃西亞
    hu = Column(Boolean, default=False)  # 匈牙利
    id = Column(Boolean, default=False)  # 印尼
    ie = Column(Boolean, default=False)  # 愛爾蘭
    il = Column(Boolean, default=False)  # 以色列
    in_ = Column(Boolean, default=False)  # 印度
    iq = Column(Boolean, default=False)  # 伊拉克
    is_ = Column(Boolean, default=False)  # 冰島
    it = Column(Boolean, default=False)  # 義大利
    jm = Column(Boolean, default=False)  # 牙買加
    jo = Column(Boolean, default=False)  # 約旦
    jp = Column(Boolean, default=False)  # 日本
    ke = Column(Boolean, default=False)  # 肯亞
    kr = Column(Boolean, default=False)  # 南韓
    kw = Column(Boolean, default=False)  # 科威特
    lb = Column(Boolean, default=False)  # 黎巴嫩
    lc = Column(Boolean, default=False)  # 聖露西亞
    li = Column(Boolean, default=False)  # 列支敦斯登
    lt = Column(Boolean, default=False)  # 立陶宛
    lu = Column(Boolean, default=False)  # 盧森堡
    lv = Column(Boolean, default=False)  # 拉脫維亞
    ly = Column(Boolean, default=False)  # 利比亞
    ma = Column(Boolean, default=False)  # 摩洛哥
    mc = Column(Boolean, default=False)  # 摩納哥
    md = Column(Boolean, default=False)  # 摩爾多瓦
    me = Column(Boolean, default=False)  # 蒙特內哥羅
    mg = Column(Boolean, default=False)  # 馬達加斯加
    mk = Column(Boolean, default=False)  # 北馬其頓
    ml = Column(Boolean, default=False)  # 馬利
    mt = Column(Boolean, default=False)  # 馬爾他
    mu = Column(Boolean, default=False)  # 模里西斯
    mx = Column(Boolean, default=False)  # 墨西哥
    my = Column(Boolean, default=False)  # 馬來西亞
    mz = Column(Boolean, default=False)  # 莫三比克
    ne = Column(Boolean, default=False)  # 尼日
    ng = Column(Boolean, default=False)  # 奈及利亞
    ni = Column(Boolean, default=False)  # 尼加拉瓜
    nl = Column(Boolean, default=False)  # 荷蘭
    no = Column(Boolean, default=False)  # 挪威
    nz = Column(Boolean, default=False)  # 紐西蘭
    om = Column(Boolean, default=False)  # 阿曼
    pa = Column(Boolean, default=False)  # 巴拿馬
    pe = Column(Boolean, default=False)  # 秘魯
    pf = Column(Boolean, default=False)  # 法屬玻里尼西亞
    ph = Column(Boolean, default=False)  # 菲律賓
    pk = Column(Boolean, default=False)  # 巴基斯坦
    pl = Column(Boolean, default=False)  # 波蘭
    ps = Column(Boolean, default=False)  # 巴勒斯坦
    pt = Column(Boolean, default=False)  # 葡萄牙
    py = Column(Boolean, default=False)  # 巴拉圭
    qa = Column(Boolean, default=False)  # 卡達
    ro = Column(Boolean, default=False)  # 羅馬尼亞
    rs = Column(Boolean, default=False)  # 塞爾維亞
    sa = Column(Boolean, default=False)  # 沙烏地阿拉伯
    sc = Column(Boolean, default=False)  # 塞席爾
    se = Column(Boolean, default=False)  # 瑞典
    sg = Column(Boolean, default=False)  # 新加坡
    si = Column(Boolean, default=False)  # 斯洛維尼亞
    sk = Column(Boolean, default=False)  # 斯洛伐克
    sm = Column(Boolean, default=False)  # 聖馬利諾
    sn = Column(Boolean, default=False)  # 塞內加爾
    sv = Column(Boolean, default=False)  # 薩爾瓦多
    tc = Column(Boolean, default=False)  # 特克斯和凱科斯群島
    td = Column(Boolean, default=False)  # 查德
    th = Column(Boolean, default=False)  # 泰國
    tn = Column(Boolean, default=False)  # 突尼西亞
    tr = Column(Boolean, default=False)  # 土耳其
    tt = Column(Boolean, default=False)  # 千里達及托巴哥
    tw = Column(Boolean, default=False)  # 台灣
    tz = Column(Boolean, default=False)  # 坦尚尼亞
    ua = Column(Boolean, default=False)  # 烏克蘭
    ug = Column(Boolean, default=False)  # 烏干達
    us = Column(Boolean, default=False)  # 美國
    uy = Column(Boolean, default=False)  # 烏拉圭
    ve = Column(Boolean, default=False)  # 委內瑞拉
    ye = Column(Boolean, default=False)  # 葉門
    za = Column(Boolean, default=False)  # 南非
    zm = Column(Boolean, default=False)  # 尚比亞
    zw = Column(Boolean, default=False)  # 辛巴威

    # 關聯
    type_rel = relationship("Type")