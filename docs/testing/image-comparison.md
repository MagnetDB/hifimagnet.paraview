# Image Comparison in Tests

Tests that generate ParaView screenshots compare them against reference images
stored under `test/Pictures/`. The comparison uses **Normalized RMSE (Root Mean
Square Error)**.

## Metric

```
nrmse = sqrt( mean( (pixel_ref - pixel_gen)^2 ) ) / 255
```

- Value is in `[0, 1]`: `0` = identical, `1` = maximally different.
- Dividing by 255 normalizes against the full 8-bit pixel range, making the
  threshold independent of image size and resolution.

This is implemented in `test/base_test.py::assert_images_equal`.

## Tolerance

Current tolerance (from `test/tolerances.py`):

| Geometry | Tolerance |
|----------|-----------|
| 2D       | 0.001     |
| 3D       | 0.001     |
| Axi      | 0.001     |

0.001 means the per-pixel RMSE must be below 0.255 intensity units on average —
a tight threshold appropriate for deterministic rendering pipelines.

If tests fail due to minor rendering differences (e.g. font rendering, OS-level
anti-aliasing, or driver version changes), consider:

1. **Regenerating reference images** on the same platform and committing them to
   `test/Pictures/`.
2. **Loosening the tolerance** in `test/tolerances.py` for the affected geometry
   type if the visual difference is acceptable (e.g. raise to `0.01` for a 1%
   allowance).

## Why Not Other Metrics?

| Metric | Issue |
|--------|-------|
| Raw sum of squared differences | Grows with image size; threshold has no intuitive meaning |
| `sqrt(sum_sq_diff)` (L2 norm) | Same problem — not bounded, not comparable to a fixed tolerance |
| SSIM | Better perceptual model but requires an extra dependency (`scikit-image`) |

Normalized RMSE is the simplest correct choice: it is bounded, size-independent,
and needs only NumPy.

## Updating Reference Images

When a rendering change is intentional, regenerate reference images by running
the test suite with the `--update-images` flag (if configured) or manually
copying the generated images from the test output directory:

```bash
cp test/cases/.../paraview.exports/views/cfpdes.expr.T.png \
   test/Pictures/2D/cfpdes.expr.T.png
```

Commit the updated references together with the code change that caused them.
