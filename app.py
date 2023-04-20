import streamlit as st
import pandas as pd
import numpy as np
import altair as alt

## cd ~/Documents/dash/v1 
## streamlit run strlit.py

## TODOs
## 1. Change the Filter
## Left : Region, Public, Iclevel, Barron's Selectivity Index, State
## Right : SAT_2013, Tuition_2013, k_median, par_q1, par_top1pc, mr_kq5_pq1, mr_ktop1_pq1, count, female, k_married, k_0inc, k_q1, k_q5, k_top1pc, scorecard_rej_rate_2013, asian_or_pacific_share_fall_2000, black_share_fall_2000, hisp_share_fall_2000, alien_share_fall_2000 

app_name = "College Exploration App"
#app_name = "Joe's Cool App"
st.set_page_config(layout="wide") # Set the page layout to wide
st.title(f"{app_name}") # Title of the app

## define CheckBoxGroup class
class CheckBoxGroup:
    def __init__(self, name, values, update_func, num_cols=1):
        self.name = name        ## variable name in the pandas dataframe
        self.values = values    ## unique values in the pandas dataframe
        self.prefix = "chk_" + name  ## prefix for the session_state variable    
        self.update_func = update_func ## function to call when the checkbox is updated
        cols = st.columns(num_cols)
        self.chk = []
        num_rows = (len(values) + num_cols - 1) // num_cols
        for i in range (len(values)):
            with cols[i // num_rows]:
                self.chk.append(st.checkbox(values[i],
                    value=True, on_change = update_func, key = self.prefix + '_' + str(i)))
#        self.chk = [st.checkbox(values[i], value=True, on_change = update_func, key = self.prefix + '_' + str(i)) for i in range(len(values))]
        st.session_state.chk_dict[self.name] = self

    ## this function is called inside the update_filter() function to get the selected items
    def get_selected_list(self):
        # scan chk_tier_0, ... chk_tier_N to see which values are selected
        chk_selected = []
        for i in range(len(self.values)):
            if st.session_state[self.prefix + '_' + str(i)]:
                chk_selected.append(self.values[i])
        return chk_selected

    ## function to reset everything to default (all checkboxes are selected)
    def reset(self):
        for i in range(len(self.values)):
            st.session_state['chk_' + self.name + '_' + str(i)] = True

@st.cache_data
def load_data(filename):
    df = pd.read_csv(filename)
    df_pct = df.rank(pct=True) * 100
    df = df.fillna(0)
    return df, df_pct

df, df_pct = load_data("mrc.merged.v2.csv")

def update_filter():
    # scan chk_tier_0, ... chk_tier_N to see which values are selected
    name2selected = {}
    for name in st.session_state.chk_dict:
        chk_box_grp = st.session_state.chk_dict[name]
        chk_selected = chk_box_grp.get_selected_list()
        name2selected[name] = chk_selected

    # update the filter
    st.session_state.df_filt = df[
                    (df['region'].isin(name2selected['region'])) &
                    (df['tier_name'].isin(name2selected['tier_name'])) &
                    (df['type'].isin(name2selected['type'])) &
                    (df['barrons'].isin(name2selected['barrons'])) &
                    (df['state'].isin(st.session_state.multi_states)) &
                    (df['sticker_price_2013'] >= st.session_state.slider_sticker_price[0]) &
                    (df['sticker_price_2013'] <= st.session_state.slider_sticker_price[1]) &
                    (df['sat_avg_2013'] >= st.session_state.slider_sat_score[0]) &
                    (df['sat_avg_2013'] <= st.session_state.slider_sat_score[1]) & 
                    (df['count'] >= st.session_state.slider_student_count[0]) &
                    (df['count'] <= st.session_state.slider_student_count[1]) & 
                    (df['par_median'] >= st.session_state.slider_par_median[0]) &
                    (df['par_median'] <= st.session_state.slider_par_median[1]) & 
                    (df['k_median'] >= st.session_state.slider_k_median[0]) &
                    (df['k_median'] <= st.session_state.slider_k_median[1]) &
                    (df['female'] >= 0.01 * st.session_state.slider_female_pct[0]) &
                    (df['female'] <= 0.01 * st.session_state.slider_female_pct[1]) & 
                    (df['scorecard_rej_rate_2013'] >= 0.01 * st.session_state.slider_rej_rate[0]) &
                    (df['scorecard_rej_rate_2013'] <= 0.01 * st.session_state.slider_rej_rate[1]) & 
                    (df['black_share_fall_2000'] >= 0.01 * st.session_state.slider_black_pct[0]) &
                    (df['black_share_fall_2000'] <= 0.01 * st.session_state.slider_black_pct[1]) &
                    (df['hisp_share_fall_2000'] >= 0.01 * st.session_state.slider_hisp_pct[0]) &
                    (df['hisp_share_fall_2000'] <= 0.01 * st.session_state.slider_hisp_pct[1]) &
                    (df['asian_or_pacific_share_fall_2000'] >= 0.01 * st.session_state.slider_asian_pct[0]) &
                    (df['asian_or_pacific_share_fall_2000'] <= 0.01 * st.session_state.slider_asian_pct[1]) & 
                    (df['alien_share_fall_2000'] >= 0.01 * st.session_state.slider_alien_pct[0]) &
                    (df['alien_share_fall_2000'] <= 0.01 * st.session_state.slider_alien_pct[1]) & 
                    (df['k_married'] >= 0.01 * st.session_state.slider_married_pct[0]) &
                    (df['k_married'] <= 0.01 * st.session_state.slider_married_pct[1])]
#    st.write(st.session_state.df_filt.shape[0])

def update_reset():
    #multi_states = state_unique_values
    st.session_state.slider_sticker_price = [0, 100000]
    st.session_state.slider_sat_score = [0, 1600]
    st.session_state.multi_states = state_unique_values
    for name in st.session_state.chk_dict:
        chk_box_grp = st.session_state.chk_dict[name]
        chk_box_grp.reset()
    update_filter()

def update_college():
    idx = df[df['name'] == st.session_state.select_college].index[0]
    st.session_state.selected_row = df.iloc[idx]
    st.session_state.selected_pct = df_pct.iloc[idx] 


axes = {'par_median' : 'Median Income of Parents at Admission (adjusted)',
        'k_median' : 'Median Income of Child at Age ~33',
        'par_q1' : 'Fraction of Parents with Bottom 20% Income',
        'par_top1pc' : 'Fraction of Parents with Top 1% Income',
        'mr_kq5_pq1' : 'Mobility Rate 20% (Parent Bottom 20% -> Child Top 20% Income)',
        'mr_ktop1_pq1' : 'Mobility Rate 1% (Parent Bottom 20% -> Child Top 1% Income)',
        'count' : 'Cohort Size',
        'sat_avg_2013' : 'SAT Average Score in 2013',
        'sticker_price_2013' : 'Annual Tuition + Fees in 2013',
        'grad_rate_150_p_2013' : 'Graduation Rate in 150% Time in 2013',
        'scorecard_netprice_2013' : 'Total Tuition + Fees for Bottom 20% Income in 2013',
        'scorecard_rej_rate_2013' : 'Fraction of Applicants Rejected in 2013',
        'trend_parq1' : 'Change in % of Parents in Bottom 20% Income',
        'trend_bottom40' : 'Change in % of Parents in Bottom 40% Income',
        'female' : 'Fraction of Female Students',
        'k_married' : 'Fraction of Students Married at age ~33',
        }

groups = {
    'tier_name' : 'College Tier',
    'type' : 'College Type',
    'public' : 'Public University',
    'barrons' : "Barron's Selectivity Index",
    'region' : 'Region',
    'czname' : 'Commuting Zone',
    'state' : 'State',
    'iclevel' : 'Degree Type',
}

#public2str = {0 : 'private', 1 : 'public'}
#iclevel2str = {1 : 'four-year', 2 : 'two-year', 3 : 'less than two-year'}

tab1, tab3, tab2, tab4, tab5 = st.tabs(["Intro", "Filters", "Visualize", "About College", "Table"])

# this is a place to store all possible values for filtering
tier_name_unique_values = sorted(list(df['tier_name'].unique()))
selectivity_unique_values = sorted(list(df['barrons'].unique()))
type_unique_values = sorted(list(df['type'].unique()))
state_unique_values = sorted(list(df['state'].unique()))
region_unique_values = sorted(list(df['region'].unique()))

# this is a place to store all the filters
if 'df_filt' not in st.session_state:
    st.session_state.df_filt = df

if 'selected_row' not in st.session_state:
    st.session_state.selected_row = df.iloc[0]

if 'selected_pct' not in st.session_state:
    st.session_state.selected_pct = df_pct.iloc[0]

if 'chk_dict' not in st.session_state:
    st.session_state.chk_dict = {}


with tab1:
    st.subheader(f"Welcome to the {app_name}!")
    st.markdown(f"#### What is the {app_name}?")
    st.write(f"The {app_name} is a tool for exploring colleges in the United States.")
    st.write("It allows you to filter colleges by various criteria and visualize the results.")
    st.write("Specifically, it allows you to:")
    st.markdown("* ***Filter*** colleges based on the selected criteria (e.g. SAT scores, tuition, median income at age ~33))")
    st.markdown("* ***Visualize*** the filtered colleges in interactive charts")
    st.markdown("* Provide ***detailed*** information on the specific college selected")
    st.markdown("* Display a ***table*** containing full information of the filtered colleges")
    st.markdown("#### Overview of the College Mobility Data")
    st.markdown("* This data track the income of students and their parents focusing on ***1980-1982 birth cohorts***")
    st.markdown("* Parental income is measured by the income of the parents at the time of the student's admission to college.")
    st.markdown("* Child income is measured by the income of the student at age ~33.")
    st.markdown("* Mobility rate is the fraction of students who move from the bottom 20% of parental income to the top 20% (or 1%) of child income.")
    st.markdown("* When year is not specified, it usually refers to the cohort of early 2000s.")
    st.markdown("* Please visit [Opportunity Insights Web Page](https://opportunityinsights.org/paper/mobilityreportcards/) for more information")

with tab2:
    st.markdown(f"#### Currently, {st.session_state.df_filt.shape[0]} colleges are selected.")

    col1, col2, col3 = st.columns(3)

    with col1:
        xaxis = st.selectbox("X-axis", axes.keys(), format_func=lambda x: axes[x], index=0)
    with col2:
        yaxis = st.selectbox("Y-axis", axes.keys(), format_func=lambda x: axes[x], index=1)
    with col3:
        group = st.selectbox("Group", groups.keys(), format_func=lambda x: groups[x], index=3)

    #st.write([xaxis, yaxis, group])

    chart = alt.Chart(df).mark_circle().encode(
        x = alt.X(xaxis, axis=alt.Axis(title=axes[xaxis])),
        y = alt.Y(yaxis, axis=alt.Axis(title=axes[yaxis])),
        opacity = alt.value(0.1),
        color = alt.value("gray"),
        tooltip=[alt.Tooltip('name', title='College Name')])

    chart_change = alt.Chart(st.session_state.df_filt).mark_point().encode(
        x = alt.X(xaxis, axis=alt.Axis(title=axes[xaxis])),
        y = alt.Y(yaxis, axis=alt.Axis(title=axes[yaxis])),
        color = alt.Color(group, legend=alt.Legend(title=groups[group])),
        tooltip = [alt.Tooltip('name', title='College Name'),
                   alt.Tooltip('par_median', title='Parent Median Income'),
                   alt.Tooltip('k_median', title='Child Median Income'),
                   alt.Tooltip('tier_name', title='College Tier'),
                   alt.Tooltip('sat_avg_2013', title='2013 SAT Average Score'),
                   alt.Tooltip('sticker_price_2013', title='2013 Tuition + Fees'),]
    )

    st.altair_chart(alt.layer(chart,chart_change).interactive(), theme="streamlit", use_container_width=True)

with tab3:
    st.markdown("### College Filter.")
    st.markdown(f"#### Currently, {st.session_state.df_filt.shape[0]} colleges are selected.")
    st.button('Reset All', key = 'reset_all', on_click = update_reset)

    col1, col2 = st.columns([5, 3], gap="large")
    with col1:
        st.markdown("#### Select Region(s)")
        cols = st.columns(2)
        chk_region = CheckBoxGroup('region', region_unique_values, update_filter, 2)
        st.markdown("#### Select College Type(s)")
        chk_type = CheckBoxGroup('type', type_unique_values, update_filter, 2)
        st.markdown("#### Select Barron's Selectivity Index")
        chk_selectivity = CheckBoxGroup('barrons', selectivity_unique_values, update_filter, 2)
        st.markdown("#### Select State(s)")
        multi_states = st.multiselect("", state_unique_values, default=state_unique_values, key = "multi_states", on_change = update_filter)
        st.markdown("#### Select College Tier(s)")
        chk_tier = CheckBoxGroup('tier_name', tier_name_unique_values, update_filter)
    with col2:
        st.markdown("#### Select Tuition & Fees (2013)")
        slider_sticker_price = st.slider("", min_value=0, max_value=55000, value=(0, 55000), step = 100, key = "slider_sticker_price", on_change = update_filter)
        st.markdown("#### Select Average SAT Score (2013)")  
        slider_sat_score = st.slider("", min_value=0, max_value=1600, value=(0, 1600), step=10, key = "slider_sat_score", on_change = update_filter)
        st.markdown("#### Select Student Count")
        slider_student_count = st.slider("", min_value=0, max_value=27000, value=(0, 27000), step=100, key = "slider_student_count", on_change = update_filter)
        st.markdown("#### Select Parent Median Income")
        slider_par_median = st.slider("", min_value=0, max_value=230000, value=(0, 230000), step=1000, key = "slider_par_median", on_change = update_filter)
        st.markdown("#### Select Child Median Income")
        slider_k_median = st.slider("", min_value=0, max_value=124000, value=(0, 124000), step=1000, key = "slider_k_median", on_change = update_filter)
        st.markdown("#### Select Female Percentage")
        slider_female_pct = st.slider("", min_value=0, max_value=100, value=(0, 100), key = "slider_female_pct", on_change = update_filter)
        st.markdown("#### Select Application Rejection Rate")
        slider_rej_rate = st.slider("", min_value=0, max_value=100, value=(0, 100), key = "slider_rej_rate", on_change = update_filter)
        st.markdown("#### Select Black Percentage")
        slider_black_pct = st.slider("", min_value=0, max_value=100, value=(0, 100), key = "slider_black_pct", on_change = update_filter)
        st.markdown("#### Select Hispanic Percentage")
        slider_hisp_pct = st.slider("", min_value=0, max_value=100, value=(0, 100), key = "slider_hisp_pct", on_change = update_filter)
        st.markdown("#### Select Asian/Pacific Percentage")
        slider_asian_pct = st.slider("", min_value=0, max_value=100, value=(0, 100), key = "slider_asian_pct", on_change = update_filter)
        st.markdown("#### Select Percentage of International Students")
        slider_alien_pct = st.slider("", min_value=0, max_value=100, value=(0, 100), key = "slider_alien_pct", on_change = update_filter)
        st.markdown("#### Select Student Married Percentage")
        slider_married_pct = st.slider("", min_value=0, max_value=100, value=(0, 100), key = "slider_married_pct", on_change = update_filter)

with tab4:
    st.markdown("#### Select or search for a college in the dropdown menu.")
    select_college = st.selectbox("", st.session_state.df_filt['name'].unique(), key = 'select_college', on_change = update_college)
    st.write("\n")
    st.write("\n")
    st.markdown(f"#### You selected : {st.session_state.select_college}")
    st.markdown(f"##### Basic Information of {st.session_state.select_college}")
    st.markdown(f"* A {st.session_state.selected_row['tier_name'].lower()} college")
    st.markdown(f"* Located in {st.session_state.selected_row['czname']}, {st.session_state.selected_row['state']}")
    st.markdown(f"* Offers a {st.session_state.selected_row['iclevel']} program.")
    st.markdown(f"##### Selectivity of {st.session_state.select_college} is {st.session_state.selected_row['barrons']}")
    st.markdown(f"##### Tuitions and fees of {st.session_state.select_college} is ${st.session_state.selected_row['sticker_price_2013']}")

with tab5:
    st.markdown(f"#### Currently, {st.session_state.df_filt.shape[0]} colleges are selected.")
    st.dataframe(st.session_state.df_filt[['name', 'czname', 'state', 'tier_name', 'sat_avg_2013', 'sticker_price_2013', 'par_median', 'k_median']])
    #st.dataframe(st.session_state.df_filt.style.highlight_max(axis=0))