import os
import sys
import json
import urllib.request
import datetime

USERNAME = "PRIY4DH4RS4N-D"
TOKEN = os.environ.get("GH_TOKEN")

def fetch_contributions_graphql():
    if not TOKEN:
        print("GH_TOKEN environment variable not set. Falling back to dummy data for generation.")
        return generate_dummy_data()

    query = """
    query {
      user(login: "%s") {
        contributionsCollection {
          contributionCalendar {
            totalContributions
            weeks {
              contributionDays {
                contributionCount
                date
                color
              }
            }
          }
        }
      }
    }
    """ % USERNAME

    req = urllib.request.Request("https://api.github.com/graphql", method="POST")
    req.add_header("Authorization", f"Bearer {TOKEN}")
    req.add_header("Content-Type", "application/json")
    
    data = json.dumps({"query": query}).encode("utf-8")
    
    try:
        with urllib.request.urlopen(req, data=data) as response:
            res_body = response.read()
            parsed = json.loads(res_body)
            return parsed['data']['user']['contributionsCollection']['contributionCalendar']
    except Exception as e:
        print(f"Error fetching from GraphQL: {e}")
        return generate_dummy_data()

def generate_dummy_data():
    # Fallback data if API fails or token is missing
    weeks = []
    import random
    for w in range(52):
        days = []
        for d in range(7):
            count = random.choice([0, 0, 0, 1, 3, 5, 10])
            days.append({"contributionCount": count})
        weeks.append({"contributionDays": days})
    return {"totalContributions": 1337, "weeks": weeks}

def generate_svg(calendar):
    weeks = calendar['weeks']
    
    # SVG Dimensions
    cell_size = 14
    cell_gap = 2
    cols = len(weeks)
    rows = 7
    
    width = cols * (cell_size + cell_gap) + 100
    height = rows * (cell_size + cell_gap) + 120
    
    svg = [
        f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {width} {height}" width="100%" height="100%">',
        '<defs>',
        '<style>',
        '@import url("https://fonts.googleapis.com/css2?family=Press+Start+2P&amp;display=swap");',
        '.bg { fill: #000000; }',
        '.text-title { fill: #ff0000; font-family: "Press Start 2P", monospace; font-size: 16px; }',
        '.text-sub { fill: #ffffff; font-family: "Press Start 2P", monospace; font-size: 10px; }',
        '.girder-0 { fill: #222222; }',
        '.girder-1 { fill: #8b0000; }',
        '.girder-2 { fill: #d32f2f; }',
        '.girder-3 { fill: #f44336; }',
        '.girder-4 { fill: #ff7961; }',
        '.ladder { stroke: #00ffff; stroke-width: 2; fill: none; }',
        '.barrel { fill: #FFA500; stroke: #8B4500; stroke-width: 2; rx: 4; }',
        '.mario { fill: #ff0000; }',
        '@keyframes roll { 0% { transform: translateX(0) rotate(0deg); } 100% { transform: translateX(600px) rotate(360deg); } }',
        '@keyframes climb { 0%, 100% { transform: translateY(0); } 50% { transform: translateY(-30px); } }',
        '</style>',
        '</defs>',
        f'<rect class="bg" width="{width}" height="{height}" />',
        f'<text x="20" y="40" class="text-title">ENGINEERING ACTIVITY</text>',
        f'<text x="20" y="65" class="text-sub">{calendar.get("totalContributions", 0)} CONTRIBUTIONS</text>',
        '<g transform="translate(20, 100)">'
    ]
    
    # Draw Girder Grid (Contributions)
    for c_idx, week in enumerate(weeks):
        for r_idx, day in enumerate(week['contributionDays']):
            count = day.get('contributionCount', 0)
            
            # Map contribution to girder level
            if count == 0: level = 0
            elif count <= 3: level = 1
            elif count <= 6: level = 2
            elif count <= 10: level = 3
            else: level = 4
                
            x = c_idx * (cell_size + cell_gap)
            y = r_idx * (cell_size + cell_gap)
            
            # Draw standard rect
            svg.append(f'<rect x="{x}" y="{y}" width="{cell_size}" height="{cell_size}" class="girder-{level}" rx="2"/>')
            
            # If it's a high contribution, add some "girder" styling lines
            if level > 0:
                svg.append(f'<line x1="{x+2}" y1="{y+2}" x2="{x+cell_size-2}" y2="{y+cell_size-2}" stroke="#000" stroke-width="1" opacity="0.3"/>')
                svg.append(f'<line x1="{x+cell_size-2}" y1="{y+2}" x2="{x+2}" y2="{y+cell_size-2}" stroke="#000" stroke-width="1" opacity="0.3"/>')

    # Draw Ladders (Decorative)
    ladders = [(5, 2), (15, 4), (25, 1), (35, 5), (45, 3)]
    for lx, ly in ladders:
        x = lx * (cell_size + cell_gap)
        y = ly * (cell_size + cell_gap)
        h = 3 * (cell_size + cell_gap)
        svg.append(f'<path class="ladder" d="M {x+4} {y} L {x+4} {y+h} M {x+10} {y} L {x+10} {y+h} M {x+4} {y+6} L {x+10} {y+6} M {x+4} {y+16} L {x+10} {y+16} M {x+4} {y+26} L {x+10} {y+26} M {x+4} {y+36} L {x+10} {y+36}" />')

    # Character (Simple SVG path approximating a retro climber)
    char_x = 10 * (cell_size + cell_gap)
    char_y = 6 * (cell_size + cell_gap)
    svg.append(f'<g transform="translate({char_x}, {char_y})" style="animation: climb 2s infinite steps(2);">')
    svg.append(f'<rect width="10" height="10" class="mario" />')
    svg.append(f'<rect x="-2" y="2" width="14" height="4" fill="#0000ff" />')
    svg.append(f'</g>')
    
    # DK Silhouette (Top left)
    svg.append('<g transform="translate(0, -30)">')
    svg.append('<rect x="0" y="0" width="30" height="30" fill="#8B4513" rx="8"/>') # Ape body
    svg.append('<rect x="5" y="5" width="20" height="15" fill="#D2B48C" rx="4"/>') # Face
    svg.append('<rect x="8" y="8" width="4" height="4" fill="#000"/>') # Eye
    svg.append('<rect x="18" y="8" width="4" height="4" fill="#000"/>') # Eye
    svg.append('</g>')

    # Animated Barrels
    for i in range(3):
        delay = i * 2.5
        y_pos = (i * 2 + 1) * (cell_size + cell_gap)
        svg.append(f'<rect class="barrel" x="0" y="{y_pos}" width="12" height="10" style="transform-origin: 6px 5px; animation: roll 5s linear infinite; animation-delay: {delay}s;" />')

    svg.append('</g>')
    svg.append('</svg>')
    
    return "\n".join(svg)

if __name__ == "__main__":
    calendar = fetch_contributions_graphql()
    svg_content = generate_svg(calendar)
    
    output_path = os.path.join(os.path.dirname(__file__), "dk-contribution.svg")
    with open(output_path, "w", encoding="utf-8") as f:
        f.write(svg_content)
    print(f"Generated {output_path}")
