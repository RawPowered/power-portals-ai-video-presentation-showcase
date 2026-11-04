"""Verify selected media identities, local links and publication boundaries."""
from pathlib import Path
from urllib.parse import unquote, urlsplit
from html.parser import HTMLParser
import hashlib, json, re
from PIL import Image

ROOT = Path(__file__).resolve().parents[1]
def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()

class Links(HTMLParser):
    def __init__(self):
        super().__init__(); self.links = []; self.ids = set()
    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        if 'id' in attrs: self.ids.add(attrs['id'])
        for key in ('href', 'src', 'poster'):
            if key in attrs: self.links.append(attrs[key])

def verify():
    errors = []; checked = 0
    documents = [ROOT/'README.md', ROOT/'RIGHTS.md', *list((ROOT/'docs').rglob('*.md')), ROOT/'assets/archive/README.md']
    parser = Links(); parser.feed((ROOT/'index.html').read_text(encoding='utf8'))
    def link(doc, target):
        nonlocal checked
        parsed = urlsplit(target.strip('<>'))
        if parsed.scheme or target.startswith('//'): return
        destination = doc.parent / unquote(parsed.path) if parsed.path else doc
        checked += 1
        if not destination.exists(): errors.append(f'Broken link: {doc.relative_to(ROOT)} -> {target}')
        if destination.name == 'index.html' and parsed.fragment and parsed.fragment not in parser.ids:
            errors.append(f'Unknown showcase anchor: {target}')
    for doc in documents:
        content = doc.read_text(encoding='utf8')
        for target in re.findall(r'\]\(([^)]+)\)', content): link(doc, target)
        embedded = Links(); embedded.feed(content)
        for target in embedded.links: link(doc, target)
    for target in parser.links: link(ROOT/'index.html', target)
    manifest = json.loads((ROOT/'evidence/public-asset-manifest.json').read_text())
    for asset in manifest['assets']:
        p = ROOT / asset['file']
        if not p.exists() or sha(p) != asset['sha256']: errors.append('Asset mismatch: '+asset['file'])
    cases = json.loads((ROOT/'evidence/critique-register.json').read_text())['cases']
    stages = json.loads((ROOT/'evidence/stage-ledger.json').read_text())['stages']
    render_hashes = {s['source_render_sha256'] for s in stages if s['source_render_sha256']}
    feedback = {x['id'] for x in json.loads((ROOT/'evidence/selected-feedback.json').read_text())['entries']}
    assert len(cases) == 17 and len(stages) == 35 and len(render_hashes) == 24
    for c in cases:
        assert (ROOT/f"docs/critiques/{c['id']}.md").exists()
        assert set(c['feedback']) <= feedback
        for side in ('before','after'):
            frame = ROOT/f"assets/frames/{c['id']}-{side}.jpg"
            metadata = json.loads(frame.with_suffix('.jpg.json').read_text())
            assert metadata['frame_sha256'] == sha(frame)
            assert metadata['source_sha256'] in render_hashes
    audio_ext = {'.wav','.mp3','.flac','.aiff','.aif','.m4a','.aac','.ogg','.wma','.opus'}
    allfiles = [p for p in ROOT.rglob('*') if p.is_file() and not set(p.relative_to(ROOT).parts) & {'.git','output','.playwright-cli','__pycache__'}]
    for p in allfiles:
        if p.suffix.lower() in audio_ext: errors.append('Standalone audio prohibited: '+str(p.relative_to(ROOT)))
        if p.stat().st_size > 95*1024*1024: errors.append('Oversized file: '+str(p.relative_to(ROOT)))
        if p.suffix.lower() in {'.png','.jpg','.gif'}:
            with Image.open(p) as image: image.verify()
        if p.suffix.lower() in {'.md','.html','.json','.yml','.py'}:
            content = p.read_text(encoding='utf8')
            if re.search(r'gh[pousr]_[A-Za-z0-9]{20,}|github_pat_[A-Za-z0-9_]{20,}|-----BEGIN (?:RSA |EC |OPENSSH )?PRIVATE KEY-----',content):
                errors.append('Credential candidate: '+str(p.relative_to(ROOT)))
    final = ROOT/'media/versions/31.mp4'
    historical = json.loads((ROOT/'evidence/final-export-verification.json').read_text())['results']
    assert sha(final) == historical['sha256']
    assert not errors, '\n'.join(errors)
    report = dict(status='passed',document_links_checked=checked,selected_media_hashes_verified=len(manifest['assets']),critique_cases=len(cases),frame_provenance_records=34,documented_stages=len(stages),historical_render_identities=len(render_hashes),final_video_bytes=final.stat().st_size,final_video_sha256=sha(final),standalone_audio_files=0,credential_candidates=0,image_integrity='passed')
    (ROOT/'evidence/publication-verification.json').write_text(json.dumps(report,indent=2)+'\n',encoding='utf8')
    print(json.dumps(report,indent=2))

if __name__ == '__main__': verify()
