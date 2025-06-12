import os
import pytest


from nipype.interfaces import dcm2nii


@pytest.mark.parametrize(
    "fname, extension, search_crop",
    [
        ("output_1", ".txt", False),
        ("output_w_[]_meta_1", ".json", False),
        ("output_w_**^$?_meta_2", ".txt", False),
        ("output_cropped", ".txt", True),
    ],
)
def test_search_files(tmp_path, fname, extension, search_crop):
    tmp_fname = fname + extension
    test_file = tmp_path / tmp_fname
    test_file.touch()
    if search_crop:
        tmp_cropped_fname = fname + "_Crop_1" + extension
        test_cropped_file = tmp_path / tmp_cropped_fname
        test_cropped_file.touch()

    actual_files_list = dcm2nii.search_files(
        str(tmp_path / fname), [extension], search_crop
    )
    for f in actual_files_list:
        if search_crop:
            assert f in (str(test_cropped_file), str(test_file))
        else:
            assert str(test_file) == f


def test_parse_stdout_windows_path():
    """Ensure ``_parse_stdout`` correctly parses Windows-style paths."""

    # ``dcm2niix`` may emit paths using backslashes when running on Windows.
    # This test mimics such output to verify the regex accepts the backslash
    # separator and the resulting path is normalized correctly.
    dcm = dcm2nii.Dcm2niix()
    line = "Convert 1 C:\\data\\file.nii"
    paths = dcm._parse_stdout(line)
    assert paths == [os.path.abspath("C:\\data\\file.nii")]
