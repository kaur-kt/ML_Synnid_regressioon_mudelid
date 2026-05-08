''' Andmete analüüs ja visualiseerimine '''


import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import matplotlib.patheffects as path_effects


### Boxplot elemendile vaates mediaanväärtuse lisamine
def add_median_labels(ax: plt.Axes, fmt: str = ".1f") -> None:
    """Add text labels to the median lines of a seaborn boxplot.

    Args:
        ax: plt.Axes, e.g. the return value of sns.boxplot()
        fmt: format string for the median value
    """
    lines = ax.get_lines()
    boxes = [c for c in ax.get_children() if "Patch" in str(c)]
    start = 4
    if not boxes:  # seaborn v0.13 => fill=False => no patches => +1 line
        boxes = [c for c in ax.get_lines() if len(c.get_xdata()) == 5]
        start += 1
    lines_per_box = len(lines) // len(boxes)
    for median in lines[start::lines_per_box]:
        x, y = (data.mean() for data in median.get_data())
        # choose value depending on horizontal or vertical plot orientation
        value = x if len(set(median.get_xdata())) == 1 else y
        text = ax.text(x, y, f'{value:{fmt}}', ha='center', va='center',
                       fontweight='bold', color='white')
        # create median-colored border around white text for contrast
        text.set_path_effects([
            path_effects.Stroke(linewidth=3, foreground=median.get_color()),
            path_effects.Normal(),
        ])
###

def analysisTheData(df):
    # Kirjeldav analüüs
    #print(df.describe())
    print("--- Analüüs ---")
    print("Kiire ülevaade: ")
    for col in df.columns:
        print(f"\n--- {col} ---")
        print(df[col].describe())
        print(df[col].value_counts().head())

    # Ristabelid
    pd.crosstab(df["Suitsetamine kokku"], df["Lapse sugu"])

    # Numbrilised tunnused
    numerical_columns = ["Raseduskestus päevades","Ema vanus","Isa vanus", "Sünnikaal", "Sünnipikkus", "Sündinud laste arv", "Vanusevahe"]
    print("Numbrilised tunnused: ")
    for col in numerical_columns:
        print(col)
        print("Miinimum:", df[col].min())
        print("Maksimum:", df[col].max())
        print("Keskmine:", df[col].mean())
        print("Mediaan:", df[col].median())
        print("Std:", df[col].std())
        print()

    #  Kategoorilised väärtused
    cathegory_columns = ["Ema perekonnaseis","Suitsetamine kokku","Lapse sugu","Sünnitusviis"]
    print("Kategoorilised tunnused: ")
    for col in cathegory_columns:
        print(f"\n{col}")
        print(df[col].value_counts())
        #print(df[col].value_counts(normalize=True) * 100)

    # Raseduskestus päevades
    print("--- graafik Raseduskestus päevades ---")
    sns.histplot(data=df, x="Raseduskestus päevades", bins=20, kde=True)
    plt.title("Raseduskestus päevades")
    plt.xlabel("Raseduskestus päevades")
    plt.ylabel("Sagedus")
    plt.show()
    #plt.show(block=False) # graafiku ekraanil näitamine ei blokeeri programmi edenemist
    #plt.pause(0.5) # väikse pausi lisamine, et graafiku renderdus jõuaks lõpule
    
    # Sünnikaal ja erindid
    # histogramm
    print("--- graafik Sünnikaal ja erindid ---")
    df["Sünnikaal"].hist(bins=30)
    plt.title("Sünnikaalu jaotus")
    plt.xlabel("Sünnikaal")
    plt.ylabel("Sagedus")
    plt.show()
    #plt.show(block=False) # graafiku ekraanil näitamine ei blokeeri programmi edenemist
    #plt.pause(0.5) # väikse pausi lisamine, et graafiku renderdus jõuaks lõpule

    # boxplot
    print("--- boxplot Sünnikaal ja erindid ---")
    ax = sns.boxplot(y=df["Sünnikaal"])
    add_median_labels(ax)
    plt.title("Sünnikaalu statistika ja erindid")
    plt.show()

    # Logaritmiliseks, kuna palju erindeid, siis suurte väärtuste mõju väiksem ja jaotus ühtlasem
    # df["Sünnikaal"] = np.log1p(df["Sünnikaal"])

    # Sünnipikkus ja erindid
    print("--- boxplot Sünnipikkuse statistika ja erindid ---")
    ax = sns.boxplot(y=df["Sünnipikkus"])
    add_median_labels(ax)
    plt.title("Sünnipikkuse statistika ja erindid")
    plt.show()
    #plt.show(block=False) # graafiku ekraanil näitamine ei blokeeri programmi edenemist
    #plt.pause(0.5) # väikse pausi lisamine, et graafiku renderdus jõuaks lõpule

    # Kategoorilised, visualiseerimine
    print("--- graafik Lapse sugu ---")
    cax = sns.countplot(x="Lapse sugu", data=df)
    for container in cax.containers:
        cax.bar_label(container)
    plt.title("Lapse sugu")
    plt.ylabel("Sagedus")
    plt.show()
    
    print("--- graafik Sünnitusviis ---")
    cax = sns.countplot(x="Sünnitusviis", data=df)
    for container in cax.containers:
        cax.bar_label(container)
    plt.title("Sünnitusviis")
    plt.ylabel("Sagedus")
    plt.xticks(rotation=45) # kallutame veidi märgendeid graafikus
    plt.show()

    # Kahe tunuse vaheliste seose uurimine
    # Numbriline ja numbriline
    # Raseduskestus päevades vs sünnikaal
    print("--- graafik Raseduskestus ja sünnikaal ---")
    sns.scatterplot(x="Raseduskestus päevades", y="Sünnikaal", data=df)
    plt.title("Raseduskestus päevades ja sünnikaal")
    plt.show()
    #plt.show(block=False) # graafiku ekraanil näitamine ei blokeeri programmi edenemist
    #plt.pause(0.5) # väikse pausi lisamine, et graafiku renderdus jõuaks lõpule
    # lineaarne trend
    print("--- graafik Sünnikaalu sõltuvus kestusest trendina ---")
    sns.regplot(x="Raseduskestus päevades", y="Sünnikaal", data=df, line_kws={"color": "red"})
    plt.title("Sünnikaalu sõltuvus raseduse kestvusest trendina")
    plt.show()
    #plt.show(block=False) # graafiku ekraanil näitamine ei blokeeri programmi edenemist
    #plt.pause(0.5) # väikse pausi lisamine, et graafiku renderdus jõuaks lõpule

    # Kategooriline ja numbriline
    # Suitsetamine kokku ja Sünnikaal
    print("--- boxplot Sünnikaalu sõltuvus suitsetamisest ---")
    ax = sns.boxplot(x="Suitsetamine kokku", y="Sünnikaal", data=df)
    add_median_labels(ax)
    #ax = set_xticklabels(["Mittesuitsetaja"], ["Suitsetaja"])
    plt.title("Sünnikaalu sõltuvus suitsetamisest")
    plt.xlabel("Võrdlus")
    plt.show()
    #plt.show(block=False) # graafiku ekraanil näitamine ei blokeeri programmi edenemist
    #plt.pause(0.5) # väikse pausi lisamine, et graafiku renderdus jõuaks lõpule
    # tulpdiagramm keskmistega
    print("--- graafik Sünnikaalu sõltuvus suitsetamisest ---")
    grp = df.groupby("Suitsetamine kokku")["Sünnikaal"].mean().plot(kind="bar")
    for container in grp.containers:
        grp.bar_label(container)
    plt.title("Keskmine sünnikaal")
    plt.xlabel("Võrdlus")
    plt.xticks(rotation=45) # kallutame märgendeid graafikus
    plt.show()
    #plt.show(block=False) # graafiku ekraanil näitamine ei blokeeri programmi edenemist
    #plt.pause(0.5) # väikse pausi lisamine, et graafiku renderdus jõuaks lõpule

    # Mitme grupi võrdlus
    # Sünnitusviis ja sünnikaal
    print("--- boxplot Sünnikaalu ja sünnitusviisi vaheline suhe ---")
    ax = sns.boxplot(x="Sünnitusviis", y="Sünnikaal", data=df)
    add_median_labels(ax)
    plt.xticks(rotation=45) # kallutame märgendeid graafikus
    plt.title("Sünnikaalu ja sünnitusviisi vaheline suhe")
    plt.show()


    return df
