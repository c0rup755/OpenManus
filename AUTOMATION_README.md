# Automated Content Creator

This system automatically creates video content using your Content Creator Studio.

## Features

- **Automated Script Generation**: Uses Abuelita Meri voice profile
- **Image Generation**: Creates cinematic images for each scene
- **Voice Generation**: Uses Edge TTS with Abuelita Meri voice settings
- **Video Creation**: Combines everything into a final video

## How to Use

### 1. Start the Content Creator Studio

```bash
cd workspace
python app.py
```

### 2. Run the Automated Content Creator

```bash
cd OpenManus
python content_creator_simple.py
```

### 3. Schedule Automated Content (Optional)

```bash
python scheduler.py
```

This will create content at:
- 9:00 AM
- 2:00 PM
- 7:00 PM

## Configuration

Edit `config/config.toml` to change:
- LLM model settings
- Browser settings
- Memory settings

## Voice Profiles

The system uses the "Abuelita Meri" voice profile by default, which includes:
- Spanish female voice (es-US-PalomaNeural)
- Slower speed (0.85 = -15% rate)
- System prompt with character specifications

## Output

Videos are saved to:
```
workspace/output/videos/
```

## Cost

- **OpenManus**: $0 (open source)
- **Gemini API**: Uses your existing API key
- **Total additional cost**: $0