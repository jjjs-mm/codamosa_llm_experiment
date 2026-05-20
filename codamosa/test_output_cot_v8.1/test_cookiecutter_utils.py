import cookiecutter.utils as module_0

def test_case_0():
    import unittest.mock as mock
    import tempfile
    import os
    import stat
    import unittest
    temp_dir = tempfile.mkdtemp()
    test_file1 = os.path.join(temp_dir, 'test_file1.txt')
    test_file2 = os.path.join(temp_dir, 'test_file2.txt')
    test_file3 = os.path.join(temp_dir, 'test_file3.txt')
    with open(test_file1, 'w') as f:
        f.write('test content 1')
    with open(test_file2, 'w') as f:
        f.write('test content 2')
    with open(test_file3, 'w') as f:
        f.write('test content 3')
    test_dir = os.path.join(temp_dir, 'test_subdir')
    os.makedirs(test_dir, exist_ok=True)
    patcher_prompt = mock.patch('cookiecutter.prompt.click.prompt', return_value=True)
    mock_prompt = patcher_prompt.start()
    try:
        var_0 = module_0.prompt_and_delete(test_file1)
        var_1 = module_0.work_in(temp_dir)
        bytes_path = test_file2.encode()
        var_2 = module_0.prompt_and_delete(bytes_path, 'test')
        var_3 = module_0.make_executable(test_file3)
        with open(test_file1, 'w') as f:
            f.write('test content 1')
        try:
            var_4 = module_0.force_delete(set(), test_file1.encode(), ())
        except TypeError:
            pass
        with open(test_file1, 'w') as f:
            f.write('test content 1')
        var_5 = module_0.force_delete(os.unlink, test_file1.encode(), {})
        try:
            var_6 = module_0.work_in(0.0)
        except TypeError:
            pass
        try:
            var_7 = module_0.force_delete(0.0, (), None)
        except TypeError:
            pass
        valid_file = os.path.join(temp_dir, 'valid_file.txt')
        with open(valid_file, 'w') as f:
            f.write('test')
        try:
            var_8 = module_0.make_sure_path_exists({valid_file})
        except TypeError:
            pass
        valid_file2 = os.path.join(temp_dir, 'valid_file2.txt')
        with open(valid_file2, 'w') as f:
            f.write('test')
        try:
            var_9 = module_0.prompt_and_delete({valid_file2}, 'test')
        except TypeError:
            pass
    finally:
        patcher_prompt.stop()
        import shutil
        shutil.rmtree(temp_dir, ignore_errors=True)

def test_case_1():
    import unittest.mock as mock
    patcher_prompt = mock.patch('cookiecutter.prompt.click.prompt', return_value=True)
    mock_prompt = patcher_prompt.start()
    try:
        str_0 = None
        set_0 = {str_0, str_0, str_0, str_0}
        var_0 = None
        try:
            var_0 = module_0.prompt_and_delete(set_0)
        except TypeError:
            pass
        str_1 = None
        bool_0 = True
        str_2 = '$\x0cW9$*.N'
        set_1 = {bool_0, var_0, str_2, frozenset(set_0)}
        list_0 = [var_0, var_0, var_0, set_1]
        str_3 = 'C8u07zcXn8DKo&ELMs'
        try:
            dict_0 = {str_1: var_0, list_0: str_3}
            int_0 = -3060
            tuple_0 = (int_0,)
            try:
                var_1 = module_0.force_delete(dict_0, tuple_0, int_0)
            except TypeError:
                pass
            try:
                var_2 = module_0.make_executable(str_0)
            except TypeError:
                pass
        except TypeError:
            pass
    finally:
        patcher_prompt.stop()

def test_case_2():
    str_0 = 'J0OR%6F4V)sV|}mUn9'
    var_0 = module_0.make_sure_path_exists(str_0)
    assert var_0 is True
    assert module_0.logger.filters == []
    assert module_0.logger.name == 'cookiecutter.utils'
    assert module_0.logger.level == 0
    assert module_0.logger.propagate is True
    assert module_0.logger.handlers == []
    assert module_0.logger.disabled is False
int_1 = -49

def test_case_4():
    import unittest.mock as mock
    import tempfile
    import os
    patcher_prompt = mock.patch('cookiecutter.prompt.click.prompt', return_value=True)
    mock_prompt = patcher_prompt.start()
    try:
        with tempfile.TemporaryDirectory() as temp_dir:
            test_file = os.path.join(temp_dir, 'test_file.txt')
            with open(test_file, 'w') as f:
                f.write('test content')
            var_0 = module_0.prompt_and_delete(test_file)
            test_dir = os.path.join(temp_dir, 'test_subdir')
            os.makedirs(test_dir, exist_ok=True)
            var_1 = module_0.prompt_and_delete(test_dir)
            set_0 = None
            try:
                var_2 = module_0.work_in(set_0)
            except TypeError:
                pass
            str_0 = 'x,=t#{\x0bHx<9A\x0b O,uyjq'
            set_1 = {str_0}
            int_0 = None
            dict_0 = {str_0: int_0}
            tuple_1 = (set_1, int_0, dict_0, int_0)
            try:
                var_3 = module_0.prompt_and_delete(tuple_1)
            except TypeError:
                pass
    finally:
        patcher_prompt.stop()

def test_case_5():
    pass

def test_case_6():
    import unittest.mock as mock
    import os
    patcher_prompt = mock.patch('cookiecutter.prompt.click.prompt', return_value=True)
    mock_prompt = patcher_prompt.start()
    isdir_patcher = mock.patch('os.path.isdir', return_value=False)
    isdir_patcher.start()
    remove_patcher = mock.patch('os.remove')
    remove_patcher.start()
    try:
        path = '/tmp/test_file.txt'
        var_0 = module_0.prompt_and_delete(path)
        bool_0 = None
        str_0 = ';gdA2-6VuD\ne'
        var_1 = module_0.force_delete(bool_0, bool_0, str_0)
        str_1 = ''
        set_0 = {var_0, var_0, str_1, path}
        var_2 = module_0.make_sure_path_exists(set_0)
    except TypeError:
        pass
    finally:
        patcher_prompt.stop()
        isdir_patcher.stop()
        remove_patcher.stop()

def test_case_7():
    int_0 = 841
    var_0 = module_0.work_in(int_0)
    assert var_0.args == (841,)
    assert var_0.kwds == {}
    assert module_0.logger.filters == []
    assert module_0.logger.name == 'cookiecutter.utils'
    assert module_0.logger.level == 0
    assert module_0.logger.propagate is True
    assert module_0.logger.handlers == []
    assert module_0.logger.disabled is False

def test_case_8():
    import unittest.mock
    import tempfile
    import os
    import shutil
    temp_dir = tempfile.mkdtemp()
    test_dir = os.path.join(temp_dir, 'test_subdir')
    os.makedirs(test_dir)
    patcher_prompt = unittest.mock.patch('cookiecutter.prompt.click.prompt', return_value=True)
    mock_prompt = patcher_prompt.start()
    try:
        var_0 = module_0.work_in()
        assert var_0.args == ()
        assert var_0.kwds == {}
        assert module_0.logger.filters == []
        assert module_0.logger.name == 'cookiecutter.utils'
        assert module_0.logger.level == 0
        assert module_0.logger.propagate is True
        assert module_0.logger.handlers == []
        assert module_0.logger.disabled is False
        var_1 = module_0.prompt_and_delete(test_dir)
        assert not os.path.exists(test_dir)
    finally:
        patcher_prompt.stop()
        shutil.rmtree(temp_dir, ignore_errors=True)

def test_case_9():
    pass