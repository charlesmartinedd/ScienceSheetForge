"""
PDF Export Functionality for ScienceSheetForge
Converts PNG worksheets to PDF format for TPT compatibility
"""
import os
from PIL import Image
import logging

logger = logging.getLogger(__name__)


def png_to_pdf(png_path, pdf_path=None):
    """
    Convert PNG worksheet to PDF format

    Args:
        png_path: Path to input PNG file
        pdf_path: Path to output PDF file (optional, auto-generated if None)

    Returns:
        str: Path to generated PDF file

    Raises:
        FileNotFoundError: If PNG file doesn't exist
        ValueError: If file conversion fails
    """
    if not os.path.exists(png_path):
        raise FileNotFoundError(f"PNG file not found: {png_path}")

    if pdf_path is None:
        pdf_path = png_path.replace('.png', '.pdf')

    try:
        # Open image and convert to RGB (PDF doesn't support RGBA)
        image = Image.open(png_path)
        if image.mode == 'RGBA':
            # Create white background
            rgb_image = Image.new('RGB', image.size, (255, 255, 255))
            rgb_image.paste(image, mask=image.split()[3])  # Use alpha channel as mask
            image = rgb_image
        elif image.mode != 'RGB':
            image = image.convert('RGB')

        # Save as PDF
        image.save(pdf_path, 'PDF', resolution=300.0, quality=95)
        logger.info(f"PDF created successfully: {pdf_path}")

        return pdf_path

    except Exception as e:
        logger.error(f"Failed to convert PNG to PDF: {e}")
        raise ValueError(f"PDF conversion failed: {e}")


def create_worksheet_bundle_pdf(png_files, output_pdf_path):
    """
    Create a multi-page PDF bundle from multiple PNG worksheets

    Args:
        png_files: List of PNG file paths
        output_pdf_path: Path for output PDF file

    Returns:
        str: Path to created PDF bundle

    Raises:
        ValueError: If no valid PNG files provided or conversion fails
    """
    if not png_files:
        raise ValueError("No PNG files provided")

    valid_files = [f for f in png_files if os.path.exists(f)]
    if not valid_files:
        raise ValueError("No valid PNG files found")

    try:
        images = []
        for png_file in valid_files:
            img = Image.open(png_file)

            # Convert to RGB
            if img.mode == 'RGBA':
                rgb_image = Image.new('RGB', img.size, (255, 255, 255))
                rgb_image.paste(img, mask=img.split()[3])
                img = rgb_image
            elif img.mode != 'RGB':
                img = img.convert('RGB')

            images.append(img)

        # Save first image and append the rest
        if len(images) == 1:
            images[0].save(output_pdf_path, 'PDF', resolution=300.0, quality=95)
        else:
            images[0].save(
                output_pdf_path,
                'PDF',
                resolution=300.0,
                quality=95,
                save_all=True,
                append_images=images[1:]
            )

        logger.info(f"PDF bundle created with {len(images)} pages: {output_pdf_path}")
        return output_pdf_path

    except Exception as e:
        logger.error(f"Failed to create PDF bundle: {e}")
        raise ValueError(f"PDF bundle creation failed: {e}")


if __name__ == '__main__':
    # Example usage
    print("PDF Export Module - Example Usage")
    print("=" * 50)
    print("To convert a single PNG to PDF:")
    print("  png_to_pdf('worksheet.png', 'worksheet.pdf')")
    print("\nTo create a multi-page PDF bundle:")
    print("  create_worksheet_bundle_pdf(['w1.png', 'w2.png'], 'bundle.pdf')")
