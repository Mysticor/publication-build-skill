# Figure

Audit actual file magic/type, vector vs raster, physical size and effective pixel resolution,
embedded fonts, clipping/bbox, labels, captions, panel letters, grayscale/color rules and naming.
Use journal-specific thresholds. raster(path,width_mm,min_dpi) reports effective DPI from pixels,
not a metadata tag. Low-resolution raster → SOURCE_REEXPORT_REQUIRED: re-export from
vector/original plotting source at required size/resolution. Upsampling/AI detail is not a fix.
Ordinary 300→600 dpi re-export, format conversion, font embedding, safe bbox and filename
changes are automatic and logged. No change to panel content, unfavorable cases or conclusions.
When color-only scientific distinctions conflict with grayscale rules and line/marker or
pattern/symbol alternatives materially affect communication, request that consequential choice.
No routine legend-position, EPS/TIFF or figure-width confirmation when rules decide.
