from skimpy import skim, generate_test_data

df = generate_test_data()
skim(df, datetime="chartreuse1")
skim(df, header_style="bold green")