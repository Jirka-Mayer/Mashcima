from mashcima.SymbolRepository import SymbolRepository
from mashcima.annotation_to_image import multi_staff_annotation_to_image \
    as _multi_staff_annotation_to_image
from typing import Optional


def use_only_writer_number_one():
    """
    Setup the default symbol repository to use only symbols of the writer 1
    """
    SymbolRepository.DEFAULT_REPOSITORY = SymbolRepository([
        "CVC-MUSCIMA_W-01_N-10_D-ideal.xml",
        "CVC-MUSCIMA_W-01_N-14_D-ideal.xml",
        "CVC-MUSCIMA_W-01_N-19_D-ideal.xml"
    ])


def synthesize(
    main_annotation: str,
    above_annotation: Optional[str] = None,
    below_annotation: Optional[str] = None,
    min_width: int = 0,
    crop_horizontally: bool = True,
    crop_vertically: bool = True,
    transform_image: bool = False,
    symbol_repository: Optional[SymbolRepository] = None
):
    """
    Synthesizes an image, using the mashcima synthesizer

    :param main_annotation str: Mashcima annotation for the main staff
        that will be synthesized.
    :param above_annotation str|None: Annotation for the staff rendered
        above the center one.
    :param below_annotation str|None: Annotation for the staff rendered
        below the center one.
    :param min_width int: Minimal width of the produced image in pixels.
        It will not be cropped below this width even if the content is
        not wide enough.
    :param crop_horizontally bool: Can be used to disable horizontal cropping.
    :param crop_vertically bool: Can be used to disable vertical cropping.
    :param transform_image bool: When true, an affine distortion is applied
        to the final image, further increasing data variability.
    :param symbol_repository SymbolRepository|None: You can provide a custom
        symbol repository to be used during the synthesis.
    """

    # if no repository was provided, use the default one
    if symbol_repository is None:
        symbol_repository = SymbolRepository.load_default()

    return _multi_staff_annotation_to_image(
        symbol_repository,
        main_annotation=main_annotation,
        above_annotation=above_annotation,
        below_annotation=below_annotation,
        min_width=min_width,
        crop_horizontally=crop_horizontally,
        crop_vertically=crop_vertically,
        transform_image=transform_image
    )
