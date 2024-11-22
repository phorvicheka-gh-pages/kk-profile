# # Skip existing files (default)
# python download_logos.py

# # Overwrite all existing files
# python download_logos.py --overwrite

# # Ask for each existing file
# python download_logos.py --ask

# # Skip existing files explicitly
# python download_logos.py --skip-existing


import requests
import os
import argparse
from pathlib import Path

# Logo URLs remain the same as previous version
logos = {
    'languages': {
        'javascript': 'https://cdn.svgporn.com/logos/javascript.svg',
        'python': 'https://cdn.svgporn.com/logos/python.svg',
        'dart': 'https://cdn.svgporn.com/logos/dart.svg',
        'kotlin': 'https://cdn.svgporn.com/logos/kotlin-icon.svg',
        'java': 'https://cdn.svgporn.com/logos/java.svg',
        'dart': 'https://cdn.svgporn.com/logos/dart.svg',
        'csharp': 'https://cdn.svgporn.com/logos/c-sharp.svg',
        'cplusplus': 'https://cdn.svgporn.com/logos/c-plusplus.svg',
        'html5': 'https://cdn.svgporn.com/logos/html-5.svg',
        'css3': 'https://cdn.svgporn.com/logos/css-3.svg',
        'php': 'https://cdn.svgporn.com/logos/php.svg'
    },
    'frontend': {
        'nextjs': 'https://cdn.svgporn.com/logos/nextjs-icon.svg',
        'flutter': 'https://cdn.svgporn.com/logos/flutter.svg',
        'android': 'https://cdn.svgporn.com/logos/android-icon.svg',
        'tailwindcss': 'https://cdn.svgporn.com/logos/tailwindcss-icon.svg',
        'figma': 'https://cdn.svgporn.com/logos/figma.svg',
        'react': 'https://cdn.svgporn.com/logos/react.svg',
        'electron': 'https://cdn.svgporn.com/logos/electron.svg',
        'svelte': 'https://cdn.svgporn.com/logos/svelte-icon.svg'
    },
    'backend': {
        'fastapi': 'https://cdn.svgporn.com/logos/fastapi-icon.svg',
        'supabase': 'https://cdn.svgporn.com/logos/supabase-icon.svg',
        'express': 'https://cdn.svgporn.com/logos/express.svg',
        'nodejs': 'https://cdn.svgporn.com/logos/nodejs-icon.svg',
        'nestjs': 'https://cdn.svgporn.com/logos/nestjs.svg',
        'springboot': 'https://cdn.svgporn.com/logos/spring-icon.svg',
        'postgresql': 'https://cdn.svgporn.com/logos/postgresql.svg',
        'laravel': 'https://cdn.svgporn.com/logos/laravel.svg',
        'mysql': 'https://cdn.svgporn.com/logos/mysql.svg'
    },
    'collaboration': {
        'git': 'https://cdn.svgporn.com/logos/git-icon.svg',
        'github': 'https://cdn.svgporn.com/logos/github-icon.svg',
        'bitbucket': 'https://cdn.svgporn.com/logos/bitbucket.svg',
        'confluence': 'https://cdn.svgporn.com/logos/confluence.svg',
        'gitlab': 'https://cdn.svgporn.com/logos/gitlab.svg',
        'jira': 'https://cdn.svgporn.com/logos/jira.svg'
    },
    'devops': {
        'docker': 'https://cdn.svgporn.com/logos/docker-icon.svg',
        'dockercompose': 'https://cdn.svgporn.com/logos/docker-icon.svg'
    },
    'aiml': {
        'claudeai': 'https://cdn.svgporn.com/logos/claude-icon.svg', # Claude AI
        'tensorflow': 'https://cdn.svgporn.com/logos/tensorflow.svg',
        'openai': 'https://cdn.svgporn.com/logos/openai-icon.svg'
    }
}

def setup_argparser():
    parser = argparse.ArgumentParser(description='Download SVG logos with overwrite options')
    parser.add_argument('--overwrite', '-o', action='store_true', 
                      help='Overwrite existing files (default: skip existing)')
    parser.add_argument('--skip-existing', '-s', action='store_true',
                      help='Skip existing files without asking (default behavior)')
    parser.add_argument('--ask', '-a', action='store_true',
                      help='Ask for each existing file')
    return parser

def download_file(url, file_path, overwrite=False, ask=False):
    if os.path.exists(file_path):
        if ask:
            response = input(f"File {file_path} exists. Overwrite? (y/N): ").lower()
            if response != 'y':
                print(f"⏭️  Skipping {file_path}")
                return False
        elif not overwrite:
            print(f"⏭️  Skipping existing file: {file_path}")
            return False
    
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    }
    
    try:
        response = requests.get(url, headers=headers, params={
            'response-content-disposition': f'attachment;filename={Path(file_path).name}'
        })
        response.raise_for_status()
        
        # Verify SVG content
        content_type = response.headers.get('content-type', '').lower()
        content_start = response.content[:100].lower()
        is_svg = ('svg' in content_type) or (b'<svg' in content_start)
        
        if not is_svg:
            print(f"⚠️  Warning: {file_path} might not be an SVG")
            
        with open(file_path, 'wb') as f:
            f.write(response.content)
        print(f"✅ Downloaded: {file_path}")
        return True
        
    except Exception as e:
        print(f"❌ Error downloading {file_path}: {str(e)}")
        return False

def download_logos(overwrite=False, ask=False):
    base_dir = 'images/logos'
    
    # Create base directory
    os.makedirs(base_dir, exist_ok=True)
    
    # Track statistics
    stats = {
        'downloaded': 0,
        'skipped': 0,
        'failed': 0,
        'total': sum(len(items) for items in logos.values())
    }
    
    # Download logos for each category
    for category, items in logos.items():
        category_dir = os.path.join(base_dir, category)
        os.makedirs(category_dir, exist_ok=True)
        
        for name, url in items.items():
            file_path = os.path.join(category_dir, f"{name}.svg")
            
            result = download_file(url, file_path, overwrite, ask)
            
            if result:
                stats['downloaded'] += 1
            else:
                if os.path.exists(file_path):
                    stats['skipped'] += 1
                else:
                    stats['failed'] += 1
    
    return stats

if __name__ == '__main__':
    parser = setup_argparser()
    args = parser.parse_args()
    
    print("\n🚀 Starting logo download from SVGPorn...")
    
    # Determine download mode
    overwrite = args.overwrite
    ask = args.ask
    
    if overwrite and ask:
        print("Warning: Both --overwrite and --ask specified. --ask will take precedence.")
        overwrite = False
    
    # Show selected mode
    mode = "ask for each file" if ask else ("overwrite existing" if overwrite else "skip existing")
    print(f"Mode: {mode}")
    
    # Download with statistics
    stats = download_logos(overwrite=overwrite, ask=ask)
    
    # Print summary
    print("\n📊 Download Summary:")
    print(f"Total files: {stats['total']}")
    print(f"Downloaded: {stats['downloaded']}")
    print(f"Skipped: {stats['skipped']}")
    print(f"Failed: {stats['failed']}")
    print("\nDownload complete! Logos are saved in 'images/logos' directory")
    