"""
Remove variables known to be dependent on 
"""

from pycytominer.cyto_utils.features import infer_cp_features

def _parse_cellprofiler(feature):
    feature_lower = feature.lower()
    if "areashape" in feature_lower and "boundingbox" in feature_lower: return True
    if "areashape" in feature_lower and "center" in feature_lower: return True
    if "_location_" in feature_lower: return True
    return False

def drop_non_bio_variant(population_df, features="infer", samples="all", drop_non_bio_variant_data_source=None):
    
    if samples != "all":
        population_df.query(samples, inplace=True)
    
    if features == "infer":
        features = infer_cp_features(population_df)
    else:
        population_df = population_df.loc[:, features]
    
    population_df_features = population_df.columns.tolist()
    
    if drop_non_bio_variant_data_source is None or not isinstance(drop_non_bio_variant_data_source, str):
        raise ValueError("data source for variant feature identification not provided or in the wrong format")
    
    if drop_non_bio_variant_data_source.lower() in ["cellprofiler", "cell_profiler"]:
        parse_feature = _parse_cellprofiler
    else:
        raise ValueError(f"data source {drop_non_bio_variant_data_source} not recognised")
    
    variant_features = [feature for feature in population_df_features if parse_feature(feature)]
    
    return variant_features