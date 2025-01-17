from attribute_class import *

def get_contained_data(df):

    complementary_info_all = []
    spatial_parameters_all = []
    temporal_parameters_all = []
    indicators_all = []

    root = tk.Tk()
    app = ColumnClassifierApp(root, df)
    root.mainloop()

    # Retrieve the result from the application
    result = app.get_result()

    # Append each list to the corresponding overall list

    spatial_parameters_all.extend(result["Spatial Parameters"])
    temporal_parameters_all.extend(result["Temporal Parameters"])
    complementary_info_all.extend(result["Complementary Information"])
    indicators_all.extend(result["Indicators"])

    return spatial_parameters_all, temporal_parameters_all, complementary_info_all, indicators_all
