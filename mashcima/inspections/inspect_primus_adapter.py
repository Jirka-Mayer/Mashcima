from mashcima.primus_adapter import load_primus_as_mashcima_annotations
from mashcima.annotation_to_image import multi_staff_annotation_to_image
from mashcima import Mashcima


def validate_all_loaded_annotations_can_be_rendered():
    mc = Mashcima(use_cache=True)
    primus = load_primus_as_mashcima_annotations(print_warnings=False)
    print("Validating...")
    print("".join(["-"] * (len(primus) // 1000)))
    for i, d in enumerate(primus):
        if i % 1000 == 0:
            print("^", end="", flush=True)
        multi_staff_annotation_to_image(mc, d["mashcima"], None, None)
    print("")


# MAIN
validate_all_loaded_annotations_can_be_rendered()
