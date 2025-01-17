from data_load import *
from load_file import *
from contained_data import *
from space_time import *
from uml_class import *
# from store_on_cloud import *
from info_theme import *

import numpy as np

code_dataset = 0

def convert_numpy_to_native(data):
    """
    Recursively convert numpy types (e.g., ndarray, int64) to native Python types.
    """
    if isinstance(data, np.ndarray):  # Convert ndarray to list
        return data.tolist()
    elif isinstance(data, (np.integer, np.int64)):  # Convert numpy integers to Python int
        return int(data)
    elif isinstance(data, (np.floating, np.float64)):  # Convert numpy floats to Python float
        return float(data)
    elif isinstance(data, dict):  # Recursively process dictionaries
        return {key: convert_numpy_to_native(value) for key, value in data.items()}
    elif isinstance(data, list):  # Recursively process lists
        return [convert_numpy_to_native(item) for item in data]
    else:  # Return other types as-is
        return data

if __name__ == "__main__":
    # Set the data source path
    all_files = get_all_files(data_source)
    datasets = []
    metadata_list = []

    # Process each file within the source
    for file_path in all_files:
        print(file_path)

        # Get identification and ingestion information
        title = os.path.basename(file_path)
        df, data_format = find_type(file_path)
        print(data_format)

        year = find_year_in_filename(os.path.basename(file_path))
        print(year)
        if year:
            df['YEAR_TITLE'] = year

        # Create identification and ingestion objects
        identification = DS_Identification(title, f"Dataset derived from {file_path}")
        ingestion = DS_Ingestion(
            dataFormat=data_format,
            fileType="file",
            updateFrequency="Unknown",
            sourceName="Data Source",
            sourceType="Public",
            sourceAddress=file_path,
        )

        # Identify the contained data into sub-classes
        spatial_parameters, temporal_parameters, cis, eis = get_contained_data(df)

        # Get spatio-temporal information
        spatialGranularity, spatialScopeLevel, spatialScope = get_space(spatial_parameters, df)
        temporalGranularity, temporalScopeLevel, temporalStart, temporalEnd = get_time(temporal_parameters, df)

        space_time = DS_Space_Time(
            space=DS_Space(
                spatialGranularity=DS_Spatial_Granularity(spatialGranularity),
                spatialScope=DS_Spatial_Scope(spatialScopeLevel, spatialScope)
            ),
            time=DS_Time(
                temporalGranularity=DS_Temporal_Granularity(temporalGranularity),
                temporalScope=DS_Temporal_Scope(temporalScopeLevel, temporalStart, temporalEnd)
            )
        )

        # Get thematic information
        theme_name = get_theme()
        theme = DS_Theme(themeCode=theme_name, themeDescription=theme_name)

        # Store dataset to the thematic catalogue according to its theme
        if theme_name:
            destination_path = theme_name.replace(" ", "_") + '/' + os.path.basename(file_path)
        else:
            destination_path = os.path.join("Uncategorized", os.path.basename(file_path))

        # 上传文件到 GCS
        # save_file_to_cloud(file_path, bucket_name, destination_path)

        # Combine all data content
        data_content = spatial_parameters + temporal_parameters + cis + eis

        # Create Dataset object
        dataset = Dataset(
            identification=identification,
            ingestion=ingestion,
            space_time=space_time,
            theme=theme,
            data_content=data_content
        )
        datasets.append(dataset)

        # Extract metadata and append to the metadata list
        metadata_entry = {
            "title": identification.title,
            "description": identification.description,
            "dataFormat": ingestion.dataFormat,
            "fileType": ingestion.fileType,
            "sourceAddress": ingestion.sourceAddress,
            "spatialGranularity": spatialGranularity,
            "spatialScopeLevel": spatialScopeLevel,
            "temporalGranularity": temporalGranularity,
            "temporalScopeLevel": temporalScopeLevel,
            "temporalScopeStart": temporalStart,
            "temporalScopeEnd": temporalEnd,
            "theme": theme.themeDescription
        }
        metadata_list.append(metadata_entry)

        # Print Dataset summary for debugging
        print("\nConstructed Dataset:")
        print(dataset.to_dict())


    # Save metadata to the specified metadata file
    metadata_list = [dataset.to_dict() for dataset in datasets]
    metadata_list_converted = [convert_numpy_to_native(metadata) for metadata in metadata_list]

    # 写入 JSON 文件
    with open(metadata_file, "w", encoding="utf-8") as meta_file:
        json.dump(metadata_list_converted, meta_file, ensure_ascii=False, indent=4)

    print("Metadata has been saved successfully.")







