import cookiecutter.utils as module_0
import os

def test_case_1():
    import sys
    import os
    import tempfile
    from unittest.mock import patch
    import cookiecutter.utils as module_0
    from cookiecutter.prompt import read_user_yes_no
    with tempfile.TemporaryDirectory() as tmp_dir:
        test_file = os.path.join(tmp_dir, 'test_file.txt')
        with open(test_file, 'w') as f:
            f.write('test content')
        patcher = patch('cookiecutter.prompt.click.prompt', return_value=True)
        patcher.start()
        try:
            var_0 = module_0.prompt_and_delete(test_file)
        finally:
            patcher.stop()
        new_test_file = os.path.join(tmp_dir, 'new_test_file.txt')
        with open(new_test_file, 'w') as f:
            f.write('test content')
        var_1 = module_0.make_executable(new_test_file)
        test_dir = os.path.join(tmp_dir, 'new_dir')
        var_2 = module_0.make_sure_path_exists(test_dir)
        var_3 = module_0.make_executable(new_test_file)
        non_existent = os.path.join(tmp_dir, 'non_existent.txt')
        with open(non_existent, 'w') as f:
            f.write('test content')
        patcher2 = patch('cookiecutter.prompt.click.prompt', return_value=True)
        patcher2.start()
        try:
            var_4 = module_0.prompt_and_delete(non_existent)
        finally:
            patcher2.stop()
        assert var_0 is True
        assert var_1 is None
        assert var_2 is True
        assert var_3 is None
        assert var_4 is True

def test_case_2():
    import sys
    sys.path.insert(0, 'replication/test-apps/cookiecutter')
    import cookiecutter.utils as module_0
    from unittest.mock import patch
    import os
    patcher_click = patch('cookiecutter.prompt.click.prompt', return_value=True)
    patcher_click.start()
    patcher = patch('cookiecutter.prompt.read_user_yes_no', return_value=True)
    patcher.start()
    try:
        with open('dummy_path', 'w') as f:
            f.write('test')
        var_0 = module_0.prompt_and_delete('dummy_path')
        assert var_0 == True
        var_1 = module_0.make_sure_path_exists('dummy_dir_1')
        assert var_1 == True
        bool_0 = True
        with open('dummy_path_2', 'w') as f:
            f.write('test')
        var_2 = module_0.prompt_and_delete('dummy_path_2')
        assert var_2 == True
        var_3 = module_0.make_sure_path_exists('dummy_dir_2')
        assert var_3 == True
        with open('dummy_path_3', 'w') as f:
            f.write('test')
        var_4 = module_0.prompt_and_delete('dummy_path_3')
        assert var_4 == True
        list_0 = ['dummy_dir_3', 'dummy_dir_4', 'dummy_dir_5']
        var_5 = module_0.make_sure_path_exists('dummy_dir_6')
        assert var_5 == True
        var_6 = module_0.work_in(list_0)
        bool_1 = False
        with open('dummy_file_1', 'w') as f:
            f.write('test')
        var_7 = module_0.make_executable('dummy_file_1')
        var_8 = module_0.make_sure_path_exists('dummy_dir_7')
        assert var_8 == True
        bool_2 = True
        with open('dummy_file_2', 'w') as f:
            f.write('test')
        var_9 = module_0.make_executable('dummy_file_2')
        module_0.make_sure_path_exists('dummy_dir_8')
        var_10 = module_0.rmtree('dummy_dir_8')
        set_0 = {'dummy_dir_9'}
        module_0.make_sure_path_exists('dummy_dir_10')
        var_11 = module_0.rmtree('dummy_dir_10')
        var_12 = module_0.work_in(set_0)
        var_13 = module_0.make_sure_path_exists('dummy_dir_11')
        assert var_13 == True
        with open('dummy_path_4', 'w') as f:
            f.write('test')
        var_14 = module_0.prompt_and_delete('dummy_path_4', 2052.6)
        assert var_14 == True
        str_0 = 'valid_path_string'
        var_15 = module_0.make_sure_path_exists(str_0)
        assert var_15 == True
    finally:
        patcher.stop()
        patcher_click.stop()

def test_case_3():
    pass

def test_case_4():
    pass

def test_case_6():
    import unittest.mock as mock
    import tempfile
    import os
    from cookiecutter import utils as module_0
    import cookiecutter.prompt as prompt_module
    with tempfile.TemporaryDirectory() as tmp_dir:
        test_path = os.path.join(tmp_dir, 'test_dir')
        os.makedirs(test_path, exist_ok=True)
        patcher = mock.patch.object(prompt_module.click, 'prompt', return_value=True)
        patcher.start()
        try:
            var_0 = module_0.prompt_and_delete(test_path)
            assert var_0 is True, 'Should return True when user confirms deletion'
            assert not os.path.exists(test_path), 'Directory should be deleted'
            non_existent = os.path.join(tmp_dir, 'non_existent')
            try:
                var_2 = module_0.prompt_and_delete(non_existent)
                assert var_2 is None, 'Should return None for non-existent path'
            except FileNotFoundError:
                pass
            test_file = os.path.join(tmp_dir, 'test_file.txt')
            with open(test_file, 'w') as f:
                f.write('test')
            var_3 = module_0.prompt_and_delete(test_file)
            assert var_3 is True, 'Should return True when deleting file'
            assert not os.path.exists(test_file), 'File should be deleted'
            bytes_path = b'/tmp/test_bytes'
            try:
                var_4 = module_0.prompt_and_delete(bytes_path)
                assert var_4 is None, 'Should handle bytes path gracefully'
            except (FileNotFoundError, TypeError):
                pass
        finally:
            patcher.stop()