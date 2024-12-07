from flask import Blueprint, request, render_template, flash, redirect
from app.utils import fetch_incidents, extract_incidents, preprocess_dataframe
from app.database import save_to_database
from app.visualizations import visualize_clustering, visualize_bar_graph, visualize_pie_chart
import pandas as pd

routes = Blueprint('routes', __name__)

@routes.route('/')
def home():
    return render_template('index.html')

from flask import render_template

@routes.route('/upload', methods=['POST'])
def upload_file():
    try:
        # Collect uploaded files
        files = request.files.getlist('files[]')
        urls = request.form.getlist('urls[]')

        # Check if at least one input is provided
        if not files and not urls:
            return render_template('index.html', error="Please upload at least one file or provide at least one URL.")

        # Initialize an empty dataframe to combine data
        combined_df = pd.DataFrame()

        # Process uploaded files
        if files:
            for file in files:
                if file:
                    file_df = extract_incidents(file)
                    combined_df = pd.concat([combined_df, file_df], ignore_index=True)

        # Process URLs
        if urls:
            for url in urls:
                if url.strip():  # Ignore empty URLs
                    pdf_path = fetch_incidents(url.strip())
                    url_df = extract_incidents(pdf_path)
                    combined_df = pd.concat([combined_df, url_df], ignore_index=True)

        # Preprocess the combined dataframe
        if combined_df.empty:
            return render_template('index.html', error="No valid data found in the provided files or URLs.")
        
        combined_df = preprocess_dataframe(combined_df)

        # Generate visualizations
        bar_graph_img = visualize_bar_graph(combined_df)
        pie_chart_img = visualize_pie_chart(combined_df)
        clustering_img = visualize_clustering(combined_df)

        # Generate stats
        stats = combined_df['nature'].value_counts().to_dict()

        return render_template(
            'visualizations.html',
            bar_graph_img=bar_graph_img,
            pie_chart_img=pie_chart_img,
            clustering_img=clustering_img,
            stats=stats,
            error=None
        )
    except KeyError as e:
        return render_template('index.html', error=f"Missing column in dataset: {str(e)}")
    except Exception as e:
        return render_template('index.html', error=f"Error processing input: {str(e)}")

@routes.route('/fetch', methods=['POST'])
def fetch_pdf():
    url = request.form['url']
    try:
        pdf_path = fetch_incidents(url)
        df = extract_incidents(pdf_path)
        db_path = 'resources/normanpd.db'
        save_to_database(df, db_path)

        # Ensure clustering only proceeds if sufficient data exists
        clustering_img = visualize_clustering(df)
        bar_graph_img = visualize_bar_graph(df)
        pie_chart_img = visualize_pie_chart(df)

        return render_template('visualizations.html', clustering_img=clustering_img, bar_graph_img=bar_graph_img, pie_chart_img=pie_chart_img)
    except Exception as e:
        # Display the error message directly in the rendered template
        return render_template('index.html', error=f"Error: {str(e)}")



