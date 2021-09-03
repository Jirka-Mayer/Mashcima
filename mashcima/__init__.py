from mashcima.CanvasOptions import CanvasOptions
from mashcima.Canvas import Canvas
from mashcima.SymbolRepository import SymbolRepository
from mashcima.annotation_to_image import multi_staff_annotation_to_image
from typing import Optional
from mashcima.generate_random_annotation import generate_random_annotation
from mashcima.primus_adapter import load_primus_as_mashcima_annotations, convert_primus_annotation_to_mashcima_annotation


def use_only_writer_number_one():
    """
    Setup the default symbol repository to use only symbols of the writer 1
    """
    SymbolRepository.DEFAULT_REPOSITORY = SymbolRepository([
        "CVC-MUSCIMA_W-01_N-10_D-ideal.xml",
        "CVC-MUSCIMA_W-01_N-14_D-ideal.xml",
        "CVC-MUSCIMA_W-01_N-19_D-ideal.xml"
    ])


def use_default_setup():
    """
    Setup the default repository back to its default settings
    """
    SymbolRepository.DEFAULT_REPOSITORY = None


def synthesize(
    main_annotation: str,
    above_annotation: Optional[str] = None,
    below_annotation: Optional[str] = None,
    
    main_canvas_options: Optional[CanvasOptions] = None,
    above_canvas_options: Optional[CanvasOptions] = None,
    below_canvas_options: Optional[CanvasOptions] = None,
    
    min_width: int = 0,
    
    crop_horizontally: bool = True,
    crop_vertically: bool = True,
    transform_image: bool = True,

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
    :param main_canvas_options CanvasOptions|None: Override canvas options
        for the main staff.
    :param above_canvas_options CanvasOptions|None: Override canvas options
        for the above staff.
    :param below_canvas_options CanvasOptions|None: Override canvas options
        for the below staff.
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

    return multi_staff_annotation_to_image(
        symbol_repository,
        main_annotation=main_annotation,
        above_annotation=above_annotation,
        below_annotation=below_annotation,
        main_canvas_options=main_canvas_options,
        above_canvas_options=above_canvas_options,
        below_canvas_options=below_canvas_options,
        min_width=min_width,
        crop_horizontally=crop_horizontally,
        crop_vertically=crop_vertically,
        transform_image=transform_image
    )


def synthesize_for_beauty(
    main_annotation: str,
    above_annotation: Optional[str] = None,
    below_annotation: Optional[str] = None,
    symbol_repository: Optional[SymbolRepository] = None
):
    """
    Calls the synthesize method with such parameters, that the resulting image
    is good looking, but may not be optimal for training
    """
    canvas_options = CanvasOptions.get_empty()
    canvas_options.random_space_probability = 0.0
    canvas_options.randomize_stem_flips_for_pitches = []

    return synthesize(
        main_annotation,
        above_annotation=above_annotation,
        below_annotation=below_annotation,

        # remove random spaces
        main_canvas_options=canvas_options,
        above_canvas_options=canvas_options,
        below_canvas_options=canvas_options,

        transform_image=False, # do not transform
        symbol_repository=symbol_repository
    )


def synthesize_for_training(
    main_annotation: str,
    above_annotation: Optional[str] = None,
    below_annotation: Optional[str] = None,
    symbol_repository: Optional[SymbolRepository] = None
):
    """
    Calls the synthesize method with such parameters, that the resulting image
    may not look nice, but the model learns robustnes on it
    """
    return synthesize(
        main_annotation,
        above_annotation=above_annotation,
        below_annotation=below_annotation,
        min_width=1200, # px
        transform_image=True, # yes, add affine transforms
        symbol_repository=symbol_repository
    )
