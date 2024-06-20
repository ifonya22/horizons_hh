import datetime
import streamlit as st
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np


def visualization():
    df = pd.read_csv('csv/clean_vac.csv', sep='\t')

    employers = set(df['Работодатель'])
    for company in employers:
        num_of_vacancies = int(len(df[df['Работодатель'] == company]))
        index_list = df[df['Работодатель'] == company].index
        df.loc[index_list, 'количество вакансий'] = num_of_vacancies

    # filters
    key_words = 'разработчик, sql'
    key_vac_name = True
    min_num_vacans = 1
    from_data = '2020-05-20'
    today = datetime.date.today()
    to_data = today.strftime('%Y-%m-%d')
    # to_data = '2024-05-20'
    location = 'москва'
    with_zp = True
    from_zp_rub = 60000
    to_zp_rub = 150000

    df['вакансия'] = df['вакансия'].str.lower()
    df['Роль'] = df['Роль'].str.lower()
    df['Локация'] = df['Локация'].str.lower()
    df['Работодатель'] = df['Работодатель'].str.lower()

    if key_vac_name:
        sub_df_1 = df[
            df['вакансия'].str.contains('|'.join(key_words.split(',')))
        ]

    df = sub_df_1
    st.title("Фильтрация вакансий")

    st.text_input("Ключевые слова", value=key_words, key="key_words")
    st.checkbox(
        "Искать в названии вакансии",
        value=key_vac_name,
        key="key_vac_name"
    )

    st.number_input(
        "Минимальное количество вакансий",
        value=min_num_vacans,
        min_value=0,
        key="min_num_vacans"
    )

    st.date_input(
        "Период от",
        value=pd.to_datetime(from_data),
        key="from_data"
    )
    st.date_input("Период до", value=pd.to_datetime(to_data), key="to_data")

    st.text_input("Локация", value=location, key="location")

    st.checkbox(
        "Показывать вакансии с зарплатой",
        value=with_zp,
        key="with_zp"
    )

    st.number_input(
        "Зарплата от (руб.)",
        value=from_zp_rub,
        min_value=0,
        key="from_zp_rub"
    )
    st.number_input(
        "Зарплата до (руб.)",
        value=to_zp_rub,
        min_value=0,
        key="to_zp_rub"
    )

    if st.button("Применить фильтры"):
        df = df[df['количество вакансий'] >= st.session_state.min_num_vacans]

        data_from = st.session_state.from_data.strftime('%Y-%m-%d')
        data_to = st.session_state.to_data.strftime('%Y-%m-%d')
        df = df[
            (df['Опубликовано'] >= data_from) & (df['Опубликовано'] <= data_to)
        ]

        if st.session_state.location != '':
            df = df[df['Локация'] == str(st.session_state.location).lower()]

        if st.session_state.with_zp:
            df.dropna(subset=['зарплата от', 'зарплата до'], inplace=True)
        df = df[(df['зарплата от'] >= st.session_state.from_zp_rub) &
                (df['зарплата до'] <= st.session_state.to_zp_rub)]
        st.write(df)

        employers = set(df['Работодатель'])
        results = {}
        for company in employers:
            num_of_vacancies = int(len(df[df['Работодатель'] == company]))
            min_list = df[df['Работодатель'] == company]['зарплата от']
            max_list = df[df['Работодатель'] == company]['зарплата до']
            median_list = list(min_list) + list(max_list)
            min_zp = np.min(min_list)
            max_zp = np.max(max_list)
            median_zp = np.median(median_list)
            mean_zp = np.mean(median_list)
            if max_zp - min_zp == 0:
                results.update(
                    {
                        company + ' (' + str(num_of_vacancies) + ')':
                        [min_zp-2200, 5000, median_zp, mean_zp]
                    }
                )
            else:
                results.update(
                    {
                        company + ' (' + str(num_of_vacancies) + ')':
                        [min_zp, max_zp - min_zp, median_zp, mean_zp]
                    }
                )

        dict_items = results.items()
        results = dict(sorted(dict_items, key=lambda x: x[1], reverse=True))

        all_market_min = min(df['зарплата от'])
        all_market_max = max(df['зарплата до'])

        all_market_median = np.median(list(df['зарплата от']) +
                                      list(df['зарплата до']))

        all_market_mean = np.mean(list(df['зарплата от']) +
                                  list(df['зарплата до']))

        results.update(
            {
                'Рынок РФ' + ' (' + str(len(df)) + ')':
                [
                    all_market_min,
                    all_market_max - all_market_min,
                    all_market_median,
                    all_market_mean
                ]
            }
        )

        diaypi_zp = 110000
        v = int(0.22*len(df))
        if int(0.22*len(df)) == 0:
            v = 1
        plt.figure(figsize=(10, v))
        labels = list(results.keys())
        data = np.array(list(results.values()))
        data_cum = data.cumsum(axis=1)
        colors = ['white', 'orange']
        medians = data[:, 2]
        means = data[:, 3]

        for i in [0, 1]:
            widths = data[:, i]
            starts = data_cum[:, i] - widths
            plt.barh(labels, widths, left=starts, height=0.7, color=colors[i])

        plt.barh(
            labels, [1000]*len(widths), left=medians, height=0.9, color='black'
        )

        plt.barh(
            labels, [1000]*len(widths), left=means, height=0.9, color='red'
        )

        plt.axvline(x=diaypi_zp)
        plt.xlim(50000, max(df['зарплата до']) + 10000)
        plt.xlabel('зарплата, руб (gross)')
        # plt.show()
        st.pyplot(plt)
