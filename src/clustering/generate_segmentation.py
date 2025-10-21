# -*- coding: utf-8 -*-
import pandas as pd
from sklearn.cluster import KMeans
import matplotlib.pyplot as plt
import seaborn as sns
from fpdf import FPDF

# Load the cleaned data from HDFS
!hdfs dfs -get /results/user_rfm/rfm.csv rfm.csv
rfm_df = pd.read_csv('rfm.csv')

# Apply KMeans clustering
kmeans = KMeans(n_clusters=4, random_state=42)
rfm_df['Cluster'] = kmeans.fit_predict(rfm_df[['Recency', 'Frequency', 'Monetary']])

# Save the clustered data back to HDFS
rfm_df.to_csv('clustered_rfm.csv', index=False)

subprocess.run(["hdfs", "dfs", "-put", "-f", "clustered_rfm.csv", "/results/user_rfm/"])
# Visualize the clusters
plt.figure(figsize=(10, 6))
sns.scatterplot(x='Recency', y='Monetary', hue='Cluster', data=rfm_df, palette='viridis')
plt.title('User Clusters based on Recency and Monetary')
plt.xlabel('Recency')
plt.ylabel('Monetary')
plt.savefig('user_clusters.png')

# Generate a PDF report
class PDF(FPDF):
    def header(self):
        self.set_font('Arial', 'B', 12)
        self.cell(0, 10, 'User Segmentation Report', 0, 1, 'C')

    def chapter_title(self, title):
        self.set_font('Arial', 'B', 12)
        self.cell(0, 10, title, 0, 1)

    def chapter_body(self, body):
        self.set_font('Arial', '', 12)
        self.multi_cell(0, 10, body)

    def print_chapter(self, num, title, body):
        self.add_page()
        self.chapter_title(title)
        self.chapter_body(body)

pdf = PDF()
pdf.print_chapter(1, 'Introduction', 'This report provides insights into user segmentation using RFM analysis.')
pdf.image('user_clusters.png', x=10, y=None, w=190, h=0, type='', link='')
pdf.output('docs/user_segmentation.pdf')

print("User segmentation report generated successfully.")




