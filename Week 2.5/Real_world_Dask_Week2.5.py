import dask.dataframe as dd
import dask.array as da
import numpy as np


def load_dataframe(file_path):
    df = dd.read_csv(file_path, delimiter="\t")
    return df


if __name__ == '__main__':

    # Load the DataFrame
    file_path = '/data/dataprocessing/interproscan/all_bacilli.tsv'
    df = load_dataframe(file_path)

    # 1- How many distinct protein annotations are found in the dataset?
    distinct_annotations = df['IPR022291'].nunique().compute()
    print("Number of distinct protein annotations:", distinct_annotations)

    # 2 How many annotations does a protein have on average?
    average_annotations_per_protein = df.groupby('gi|29898682|gb|AAP11954.1|')[
        'IPR022291'].count().mean().compute()
    print("Average number of annotations per protein:",
          average_annotations_per_protein)

    # 3 What is the most common GO Term found?
    most_common_go_term = df['TIGRFAM'].mode().compute()
    print("Most common GO Term:", most_common_go_term)

    # 4 What is the average size of an InterPRO feature found in the dataset?
    average_interpro_feature_size = df['547'].mean().compute()
    print("Average size of InterPRO feature:", average_interpro_feature_size)

    # 5 What is the top 10 most common InterPRO features?
    top_10_common_interpro_features = df['TIGR03882'].value_counts().nlargest(
        10).compute()
    print("Top 10 most common InterPRO features:")
    print(top_10_common_interpro_features)

    # 7 If you look at those features which also have textual annotation, what is the top 10 most common word found in that annotation?
    annotated_interpro_features = df[df['TIGR03882'].notnull(
    )]['cyclo_dehyd_2: bacteriocin biosynthesis cyclodehydratase domain']
    top_10_common_words_in_annotation = annotated_interpro_features.str.split(
    ).explode().value_counts().nlargest(10).compute()
    print("Top 10 most common words in annotation:")
    print(top_10_common_words_in_annotation)

    # 8  what is the top 10 least common word found in that annotation?

    annotated_interpro_features = df[df['TIGR03882'].notnull(
    )]['cyclo_dehyd_2: bacteriocin biosynthesis cyclodehydratase domain']
    top_10_least_common_words_in_annotation = annotated_interpro_features.str.split(
    ).explode().value_counts().tail(10)
    print("Top 10 least common words in annotation:")
    print(top_10_least_common_words_in_annotation)

    # # 6 If you select InterPRO features that are almost the same size (within 90-100%) as the protein itself, what is the top 10 then?
    # protein_size = df['92d1264e347e149248231cb9b649388c'].astype(str)
    # protein_size = protein_size[protein_size.notnull()]  # Filter out non-numeric values
    # selected_interpro_features = df[(protein_size.notnull()) & (df['547'] >= protein_size * 0.9) & (df['547'] <= protein_size * 1.0)]['TIGR03882']
    # top_10_common_selected_interpro_features = selected_interpro_features.value_counts().nlargest(10).compute()
    # print("Top 10 most common selected InterPRO features:")
    # print(top_10_common_selected_interpro_features)

    # # 10 What is the coefficient of correlation between the size of the protein and the number of features found?
    # correlation_coefficient = da.correlate(protein_size.to_dask_array(lengths=True), df['TIGR03882'].to_dask_array(lengths=True), dtype=np.float64).compute()
    # print("Correlation coefficient between protein size and number of features:", correlation_coefficient)

# Fatemeh and me did this assignment together.
