import os
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from dython.nominal import associations


def createReports():

    df = loadDataframeFromCSV('data','bank-full.csv')

    dfUsefulColumns = removeColums(df, ['contact','day','month','duration','campaign','pdays','previous','poutcome'])

    columnsStatisticsExploration(dfUsefulColumns)

    targetStatisticsExploration(dfUsefulColumns)

    plotIndipendentVariableCorrelation(dfUsefulColumns)

    plotIndipendentVariableTargetCorrelation(dfUsefulColumns)

    ageAnalisys(dfUsefulColumns)



def plotIndipendentVariableCorrelation(dfUsefulColumns: pd.DataFrame):
    # correlation between categorical variables using CramersV method
    dfUsefulIndipendentColumns = dfUsefulColumns.drop(columns='y', inplace=False)
    correlation_variable_target_dict = associations(dfUsefulIndipendentColumns, nom_nom_assoc="cramer", nominal_columns='auto',
                 compute_only=True)

    corr_matrix = correlation_variable_target_dict['corr']

    plt.figure(figsize=(8, 6))
    sns.heatmap(corr_matrix, annot=True, cmap='coolwarm', fmt=".2f")
    plt.title("Indipendent Variable Correlation (Cramer's V)")
    plt.tight_layout()

    plt.savefig("picture/Indipendent_Variable_Correlation.jpg", dpi=300, bbox_inches='tight')
    plt.close()

    print("Correlation Heatmap saved in Indipendent Variable Correlation.jpg")



def ageAnalisys(df: pd.DataFrame):

    sns.set_style("whitegrid")

    plt.figure(figsize=(8, 5))
    sns.histplot(df['age'], bins=100, kde=False, color='steelblue', edgecolor='black')
    plt.title(f"Age's Distribution")
    plt.xlabel('Age')
    plt.ylabel("Frequence")

    plt.tight_layout()
    plt.savefig('picture/Age_distribution.jpg', dpi=300, bbox_inches='tight')
    plt.close()

    print("Histogram saved as Age_distribution.jpg")



def plotIndipendentVariableTargetCorrelation(dfUsefulColumns: pd.DataFrame):

    correlation_variable_target_dict = associations(
        dfUsefulColumns,
        nom_nom_assoc="cramer",
        nominal_columns='auto',
        compute_only=True
    )

    corr_matrix = correlation_variable_target_dict['corr']
    target_corr = corr_matrix['y'].drop('y')

    plt.figure(figsize=(6, 4))
    target_corr.sort_values(ascending=True).plot(kind='barh', color='cornflowerblue')
    plt.title("Cramer's Correlation with: target")
    plt.xlabel("Cramer's Correlation")
    plt.tight_layout()

    plt.savefig("picture/Correlation_Indipendent_Variable_Target.jpg", dpi=300, bbox_inches='tight')
    plt.close()

    print("Correlation Map saved as Correlation_Indipendent_Variable_Target.jpg")




def loadDataframeFromCSV (folderName: str, fileName: str) -> pd.DataFrame:
    try:

        scriptDir = os.path.dirname(os.path.abspath(__file__))
        projectRoot = os.path.dirname(scriptDir)
        filePath = os.path.join(projectRoot, '..', folderName, fileName)

        print(f"\nLooking schema at this path: {filePath}")

        df = pd.read_csv(filePath, sep=";")

        print("File Correctly read")
        return df

    except FileNotFoundError:
        print(f"\nERROR schema not found at this path: {filePath}!")
    except Exception as e:
        print(f"Unexpected exception during csv reading: {e}")



def removeColums(df: pd.DataFrame, columnsToRemove: list[str]) -> pd.DataFrame:
    try:
        return df.drop(columnsToRemove, axis=1)
    except Exception as e:
        print(f"Unexpected exception during unuseful columns removal: {e}")



def columnsStatisticsExploration(dfUsefulColumns: pd.DataFrame):

    num_cols = dfUsefulColumns.select_dtypes(include=["number"]).columns
    cat_cols = dfUsefulColumns.select_dtypes(include=["object", "category", "bool"]).columns

    desc_num = dfUsefulColumns[num_cols].describe()
    desc_cat = dfUsefulColumns[cat_cols].describe()

    nulls_num = dfUsefulColumns[num_cols].isna().sum()
    nulls_cat = dfUsefulColumns[cat_cols].isna().sum()

    desc_num.loc["null_count"] = nulls_num
    desc_cat.loc["null_count"] = nulls_cat

    desc_num.loc["null_%"] = (nulls_num / len(dfUsefulColumns)) * 100
    desc_cat.loc["null_%"] = (nulls_cat / len(dfUsefulColumns)) * 100

    with pd.ExcelWriter("schema/overall_description.xlsx", engine="xlsxwriter") as writer:
        desc_num.to_excel(writer, sheet_name="Numerical")
        desc_cat.to_excel(writer, sheet_name="Categorical")

    print("File 'overall_description.xlsx' created!")



def targetStatisticsExploration(dfUsefulColumns: pd.DataFrame):
    col = "y"
    plt.figure(figsize=(6, 4))
    sns.histplot(data=dfUsefulColumns, x=col, bins=30, line_kws=None, color="steelblue", edgecolor="white")
    plt.title("Target Distribution")
    plt.xlabel("Values")
    plt.ylabel("Frequence")
    plt.tight_layout()
    plt.savefig("picture/Target_distribution.jpg", format="jpg", dpi=300)
    plt.close()

    print("File Target_distribution.jpg created!")



if __name__ == "__main__":
    createReports()