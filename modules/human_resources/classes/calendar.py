from configuration import classes_names
def create_table():
    GenerateDateSeries = "CREATE TABLE "+classes_names.calendar+" AS ( select date::date, extract('isodow' from date) as dow," \
                     "       to_char(date, 'dy') as day," \
                     "       extract('week' from date) as week," \
                     "       extract ('MONTH'from date )as month," \
                     "       extract('year' from date) as year," \
                     "       extract('day' from" \
                     "               (date + interval '2 month - 1 day')              ) = 29       as leap" \
                     "  from generate_series(timestamp  without time zone '2019-01-01'," \
                     "                       timestamp  without time zone'2025-12-30'," \
                     "                      interval '1 day')as t(date));" \
                     "       ALTER TABLE "+classes_names.calendar+" ADD COLUMN holiday BOOLEAN DEFAULT FALSE ;" \
                     "       ALTER TABLE "+classes_names.calendar+" ADD COLUMN id SERIAL PRIMARY KEY;    " \
                     "        ALTER TABLE "+classes_names.calendar+" ADD COLUMN metadata json ;       "


    return GenerateDateSeries

