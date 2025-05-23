import pandas as pd
import matplotlib.pyplot as plt

# Load the data
df = pd.read_excel('/content/faculty_ratings (1).xlsx')

# Clean faculty names (remove section prefixes)
df['Faculty Name'] = df['Faculty Name'].str.replace(r'^Section[-\s]\w+-', '', regex=True).str.strip()

# Clean rating categories (remove trailing numbers and instructions)
df['Rating Category'] = df['Rating Category'].str.split('(', n=1, expand=True)[0].str.strip()

# Clean course names (remove "Feedback on ")
df['Course'] = df['Course'].str.replace(r'^Feedback on\s+', '', regex=True).str.strip()

# Group data by faculty and calculate average ratings
faculty_data = df.groupby(['Faculty Name', 'Rating Category'])['Rating'].mean().round(4).reset_index()

# Get unique courses per faculty
courses_per_faculty = df.groupby('Faculty Name')['Course'].unique().apply(list).to_dict()

# Create individual PNG images for each faculty
for faculty in faculty_data['Faculty Name'].unique():
    # Filter data for current faculty
    faculty_df = faculty_data[faculty_data['Faculty Name'] == faculty]

    # Calculate total average
    total_avg = faculty_df['Rating'].mean().round(4)

    # Create new row for total average
    new_row = pd.DataFrame({
        'Rating Category': ['Total Average'],
        'Rating': [total_avg]
    })

    # Append new row to faculty_df
    faculty_df = pd.concat([faculty_df, new_row], ignore_index=True)

    # Prepare data for table
    headers = ['Rating Category', 'Average Rating']
    data = faculty_df[['Rating Category', 'Rating']].values.tolist()

    # Add course list as a header row
    course_list = ', '.join(courses_per_faculty.get(faculty, []))
    data.insert(0, ['Courses Taught:', course_list])

    # Create figure and axis
    fig, ax = plt.subplots(figsize=(8, 6))
    ax.axis('off')  # Hide axes

    # Create table
    table = ax.table(
        cellText=data,
        colLabels=headers,
        loc='center',
        cellLoc='left',
        colWidths=[0.7, 0.3]
    )

    # Set font size and padding
    table.auto_set_font_size(False)
    table.set_fontsize(12)
    table.scale(1, 1.5)

    # Save as PNG image
    filename = f"{faculty.replace(' ', '_')}_ratings.png"
    plt.savefig(filename, bbox_inches='tight')
    plt.close()

print("Individual PNG images created successfully!")
