import logging
import pandas as pd
from datetime import datetime
from .models import Type, Movie
from .database_manager import DatabaseManager

logging.basicConfig(
    level=logging.INFO
)

class NetflixETL:
    def __init__(self, csv_path):
        logging.info(f"Start ETL, csv Path: {csv_path}")
        try:
            self.df = pd.read_csv(
                csv_path,
                low_memory=False,
                dtype = {
                    'releaseYear': 'Int64',
                    'imdbNumVotes': 'Int64'
                }
            )
            logging.info(f"load {len(self.df)} rows from csv")
        except Exception as e:
            logging.error(f'Fail to load csv: {e}')

        self.db_manager = DatabaseManager()
        self.db_manager.initialize_database()
    
    def transform_data(self):
        logging.info('Start transforming data from csv to SQLite...')
        with self.db_manager.get_db_session() as session:

            try:
                # Types
                types = {}
                for _, row in self.df.iterrows():
                    if row['type'] not in types:
                        type = Type(
                            type=row['type']
                        )
                        session.add(type)
                        types[row['type']] = type

                session.flush()

                # Movies
                movies = []
                for _, row in self.df.iterrows():
                    movie = Movie(
                        imdb_id=row['imdbId'],
                        title=row['title'],
                        type_id=types[row['type']].id,
                        release_year=row['releaseYear'],
                        imdb_average_rating=row['imdbAverageRating'],
                        imdb_num_votes=row['imdbNumVotes'],
                        action=row['Action'],
                        adult=row['Adult'],
                        adventure=row['Adventure'],
                        animation=row['Animation'],
                        biography=row['Biography'],
                        comedy=row['Comedy'],
                        crime=row['Crime'],
                        documentary=row['Documentary'],
                        drama=row['Drama'],
                        family=row['Family'],
                        fantasy=row['Fantasy'],
                        film_noir=row['Film-Noir'],
                        game_show=row['Game-Show'],
                        history=row['History'],
                        horror=row['Horror'],
                        music=row['Music'],
                        musical=row['Musical'],
                        mystery=row['Mystery'],
                        news=row['News'],
                        reality_tv=row['Reality-TV'],
                        romance=row['Romance'],
                        sci_fi=row['Sci-Fi'],
                        short=row['Short'],
                        sport=row['Sport'],
                        talk_show=row['Talk-Show'],
                        thriller=row['Thriller'],
                        war=row['War'],
                        western=row['Western'],
                        ad=row['AD'],
                        ae=row['AE'],
                        ag=row['AG'],
                        al=row['AL'],
                        ao=row['AO'],
                        ar=row['AR'],
                        at=row['AT'],
                        au=row['AU'],
                        az=row['AZ'],
                        ba=row['BA'],
                        bb=row['BB'],
                        be=row['BE'],
                        bg=row['BG'],
                        bh=row['BH'],
                        bm=row['BM'],
                        bo=row['BO'],
                        br=row['BR'],
                        bs=row['BS'],
                        by=row['BY'],
                        bz=row['BZ'],
                        ca=row['CA'],
                        ch=row['CH'],
                        ci=row['CI'],
                        cl=row['CL'],
                        cm=row['CM'],
                        co=row['CO'],
                        cr=row['CR'],
                        cu=row['CU'],
                        cv=row['CV'],
                        cy=row['CY'],
                        cz=row['CZ'],
                        de=row['DE'],
                        dk=row['DK'],
                        do=row['DO'],
                        dz=row['DZ'],
                        ec=row['EC'],
                        ee=row['EE'],
                        eg=row['EG'],
                        es=row['ES'],
                        fi=row['FI'],
                        fj=row['FJ'],
                        fr=row['FR'],
                        gb=row['GB'],
                        gf=row['GF'],
                        gg=row['GG'],
                        gh=row['GH'],
                        gi=row['GI'],
                        gq=row['GQ'],
                        gr=row['GR'],
                        gt=row['GT'],
                        hk=row['HK'],
                        hn=row['HN'],
                        hr=row['HR'],
                        hu=row['HU'],
                        id=row['ID'],
                        ie=row['IE'],
                        il=row['IL'],
                        in_=row['IN'],
                        iq=row['IQ'],
                        is_=row['IS'],
                        it=row['IT'],
                        jm=row['JM'],
                        jo=row['JO'],
                        jp=row['JP'],
                        ke=row['KE'],
                        kr=row['KR'],
                        kw=row['KW'],
                        lb=row['LB'],
                        lc=row['LC'],
                        li=row['LI'],
                        lt=row['LT'],
                        lu=row['LU'],
                        lv=row['LV'],
                        ly=row['LY'],
                        ma=row['MA'],
                        mc=row['MC'],
                        md=row['MD'],
                        me=row['ME'],
                        mg=row['MG'],
                        mk=row['MK'],
                        ml=row['ML'],
                        mt=row['MT'],
                        mu=row['MU'],
                        mx=row['MX'],
                        my=row['MY'],
                        mz=row['MZ'],
                        ne=row['NE'],
                        ng=row['NG'],
                        ni=row['NI'],
                        nl=row['NL'],
                        no=row['NO'],
                        nz=row['NZ'],
                        om=row['OM'],
                        pa=row['PA'],
                        pe=row['PE'],
                        pf=row['PF'],
                        ph=row['PH'],
                        pk=row['PK'],
                        pl=row['PL'],
                        ps=row['PS'],
                        pt=row['PT'],
                        py=row['PY'],
                        qa=row['QA'],
                        ro=row['RO'],
                        rs=row['RS'],
                        sa=row['SA'],
                        sc=row['SC'],
                        se=row['SE'],
                        sg=row['SG'],
                        si=row['SI'],
                        sk=row['SK'],
                        sm=row['SM'],
                        sn=row['SN'],
                        sv=row['SV'],
                        tc=row['TC'],
                        td=row['TD'],
                        th=row['TH'],
                        tn=row['TN'],
                        tr=row['TR'],
                        tt=row['TT'],
                        tw=row['TW'],
                        tz=row['TZ'],
                        ua=row['UA'],
                        ug=row['UG'],
                        us=row['US'],
                        uy=row['UY'],
                        ve=row['VE'],
                        ye=row['YE'],
                        za=row['ZA'],
                        zm=row['ZM'],
                        zw=row['ZW']
                    )
                    movies.append(movie)

                # 將 NAType 轉換為 None
                for movie in movies:
                    for key, value in movie.__dict__.items():
                        if pd.isna(value):
                            setattr(movie, key, None)
                session.bulk_save_objects(movies)
            except Exception as e:
                logging.error('Fail to transform data.')
                raise

    def process(self):
        self.transform_data()

def main():
    etl = NetflixETL("./data/netflix_processed.csv")
    etl.process()

if __name__ == "__main__":
    main()   