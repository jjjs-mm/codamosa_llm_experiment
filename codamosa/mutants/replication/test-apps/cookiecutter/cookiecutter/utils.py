"""Helper functions used throughout Cookiecutter."""
import contextlib
import errno
import logging
import os
import shutil
import stat
import sys

from cookiecutter.prompt import read_user_yes_no

logger = logging.getLogger(__name__)
from typing import Annotated
from typing import Callable
from typing import ClassVar

MutantDict = Annotated[dict[str, Callable], "Mutant"] # type: ignore


def _mutmut_trampoline(orig, mutants, call_args, call_kwargs, self_arg = None): # type: ignore
    """Forward call to original or mutated function, depending on the environment"""
    import os # type: ignore
    mutant_under_test = os.environ['MUTANT_UNDER_TEST'] # type: ignore
    if mutant_under_test == 'fail': # type: ignore
        from mutmut.__main__ import MutmutProgrammaticFailException # type: ignore
        raise MutmutProgrammaticFailException('Failed programmatically')       # type: ignore
    elif mutant_under_test == 'stats': # type: ignore
        from mutmut.__main__ import record_trampoline_hit # type: ignore
        record_trampoline_hit(orig.__module__ + '.' + orig.__name__) # type: ignore
        # (for class methods, orig is bound and thus does not need the explicit self argument)
        result = orig(*call_args, **call_kwargs) # type: ignore
        return result # type: ignore
    prefix = orig.__module__ + '.' + orig.__name__ + '__mutmut_' # type: ignore
    if not mutant_under_test.startswith(prefix): # type: ignore
        result = orig(*call_args, **call_kwargs) # type: ignore
        return result # type: ignore
    mutant_name = mutant_under_test.rpartition('.')[-1] # type: ignore
    if self_arg is not None: # type: ignore
        # call to a class method where self is not bound
        result = mutants[mutant_name](self_arg, *call_args, **call_kwargs) # type: ignore
    else:
        result = mutants[mutant_name](*call_args, **call_kwargs) # type: ignore
    return result # type: ignore


def force_delete(func, path, exc_info):
    args = [func, path, exc_info]# type: ignore
    kwargs = {}# type: ignore
    return _mutmut_trampoline(x_force_delete__mutmut_orig, x_force_delete__mutmut_mutants, args, kwargs, None)


def x_force_delete__mutmut_orig(func, path, exc_info):
    """Error handler for `shutil.rmtree()` equivalent to `rm -rf`.

    Usage: `shutil.rmtree(path, onerror=force_delete)`
    From https://docs.python.org/3/library/shutil.html#rmtree-example
    """
    os.chmod(path, stat.S_IWRITE)
    func(path)


def x_force_delete__mutmut_1(func, path, exc_info):
    """Error handler for `shutil.rmtree()` equivalent to `rm -rf`.

    Usage: `shutil.rmtree(path, onerror=force_delete)`
    From https://docs.python.org/3/library/shutil.html#rmtree-example
    """
    os.chmod(None, stat.S_IWRITE)
    func(path)


def x_force_delete__mutmut_2(func, path, exc_info):
    """Error handler for `shutil.rmtree()` equivalent to `rm -rf`.

    Usage: `shutil.rmtree(path, onerror=force_delete)`
    From https://docs.python.org/3/library/shutil.html#rmtree-example
    """
    os.chmod(path, None)
    func(path)


def x_force_delete__mutmut_3(func, path, exc_info):
    """Error handler for `shutil.rmtree()` equivalent to `rm -rf`.

    Usage: `shutil.rmtree(path, onerror=force_delete)`
    From https://docs.python.org/3/library/shutil.html#rmtree-example
    """
    os.chmod(stat.S_IWRITE)
    func(path)


def x_force_delete__mutmut_4(func, path, exc_info):
    """Error handler for `shutil.rmtree()` equivalent to `rm -rf`.

    Usage: `shutil.rmtree(path, onerror=force_delete)`
    From https://docs.python.org/3/library/shutil.html#rmtree-example
    """
    os.chmod(path, )
    func(path)


def x_force_delete__mutmut_5(func, path, exc_info):
    """Error handler for `shutil.rmtree()` equivalent to `rm -rf`.

    Usage: `shutil.rmtree(path, onerror=force_delete)`
    From https://docs.python.org/3/library/shutil.html#rmtree-example
    """
    os.chmod(path, stat.S_IWRITE)
    func(None)

x_force_delete__mutmut_mutants : ClassVar[MutantDict] = { # type: ignore
'x_force_delete__mutmut_1': x_force_delete__mutmut_1, 
    'x_force_delete__mutmut_2': x_force_delete__mutmut_2, 
    'x_force_delete__mutmut_3': x_force_delete__mutmut_3, 
    'x_force_delete__mutmut_4': x_force_delete__mutmut_4, 
    'x_force_delete__mutmut_5': x_force_delete__mutmut_5
}
x_force_delete__mutmut_orig.__name__ = 'x_force_delete'


def rmtree(path):
    args = [path]# type: ignore
    kwargs = {}# type: ignore
    return _mutmut_trampoline(x_rmtree__mutmut_orig, x_rmtree__mutmut_mutants, args, kwargs, None)


def x_rmtree__mutmut_orig(path):
    """Remove a directory and all its contents. Like rm -rf on Unix.

    :param path: A directory path.
    """
    shutil.rmtree(path, onerror=force_delete)


def x_rmtree__mutmut_1(path):
    """Remove a directory and all its contents. Like rm -rf on Unix.

    :param path: A directory path.
    """
    shutil.rmtree(None, onerror=force_delete)


def x_rmtree__mutmut_2(path):
    """Remove a directory and all its contents. Like rm -rf on Unix.

    :param path: A directory path.
    """
    shutil.rmtree(path, onerror=None)


def x_rmtree__mutmut_3(path):
    """Remove a directory and all its contents. Like rm -rf on Unix.

    :param path: A directory path.
    """
    shutil.rmtree(onerror=force_delete)


def x_rmtree__mutmut_4(path):
    """Remove a directory and all its contents. Like rm -rf on Unix.

    :param path: A directory path.
    """
    shutil.rmtree(path, )

x_rmtree__mutmut_mutants : ClassVar[MutantDict] = { # type: ignore
'x_rmtree__mutmut_1': x_rmtree__mutmut_1, 
    'x_rmtree__mutmut_2': x_rmtree__mutmut_2, 
    'x_rmtree__mutmut_3': x_rmtree__mutmut_3, 
    'x_rmtree__mutmut_4': x_rmtree__mutmut_4
}
x_rmtree__mutmut_orig.__name__ = 'x_rmtree'


def make_sure_path_exists(path):
    args = [path]# type: ignore
    kwargs = {}# type: ignore
    return _mutmut_trampoline(x_make_sure_path_exists__mutmut_orig, x_make_sure_path_exists__mutmut_mutants, args, kwargs, None)


def x_make_sure_path_exists__mutmut_orig(path):
    """Ensure that a directory exists.

    :param path: A directory path.
    """
    logger.debug('Making sure path exists: %s', path)
    try:
        os.makedirs(path)
        logger.debug('Created directory at: %s', path)
    except OSError as exception:
        if exception.errno != errno.EEXIST:
            return False
    return True


def x_make_sure_path_exists__mutmut_1(path):
    """Ensure that a directory exists.

    :param path: A directory path.
    """
    logger.debug(None, path)
    try:
        os.makedirs(path)
        logger.debug('Created directory at: %s', path)
    except OSError as exception:
        if exception.errno != errno.EEXIST:
            return False
    return True


def x_make_sure_path_exists__mutmut_2(path):
    """Ensure that a directory exists.

    :param path: A directory path.
    """
    logger.debug('Making sure path exists: %s', None)
    try:
        os.makedirs(path)
        logger.debug('Created directory at: %s', path)
    except OSError as exception:
        if exception.errno != errno.EEXIST:
            return False
    return True


def x_make_sure_path_exists__mutmut_3(path):
    """Ensure that a directory exists.

    :param path: A directory path.
    """
    logger.debug(path)
    try:
        os.makedirs(path)
        logger.debug('Created directory at: %s', path)
    except OSError as exception:
        if exception.errno != errno.EEXIST:
            return False
    return True


def x_make_sure_path_exists__mutmut_4(path):
    """Ensure that a directory exists.

    :param path: A directory path.
    """
    logger.debug('Making sure path exists: %s', )
    try:
        os.makedirs(path)
        logger.debug('Created directory at: %s', path)
    except OSError as exception:
        if exception.errno != errno.EEXIST:
            return False
    return True


def x_make_sure_path_exists__mutmut_5(path):
    """Ensure that a directory exists.

    :param path: A directory path.
    """
    logger.debug('XXMaking sure path exists: %sXX', path)
    try:
        os.makedirs(path)
        logger.debug('Created directory at: %s', path)
    except OSError as exception:
        if exception.errno != errno.EEXIST:
            return False
    return True


def x_make_sure_path_exists__mutmut_6(path):
    """Ensure that a directory exists.

    :param path: A directory path.
    """
    logger.debug('making sure path exists: %s', path)
    try:
        os.makedirs(path)
        logger.debug('Created directory at: %s', path)
    except OSError as exception:
        if exception.errno != errno.EEXIST:
            return False
    return True


def x_make_sure_path_exists__mutmut_7(path):
    """Ensure that a directory exists.

    :param path: A directory path.
    """
    logger.debug('MAKING SURE PATH EXISTS: %S', path)
    try:
        os.makedirs(path)
        logger.debug('Created directory at: %s', path)
    except OSError as exception:
        if exception.errno != errno.EEXIST:
            return False
    return True


def x_make_sure_path_exists__mutmut_8(path):
    """Ensure that a directory exists.

    :param path: A directory path.
    """
    logger.debug('Making sure path exists: %s', path)
    try:
        os.makedirs(None)
        logger.debug('Created directory at: %s', path)
    except OSError as exception:
        if exception.errno != errno.EEXIST:
            return False
    return True


def x_make_sure_path_exists__mutmut_9(path):
    """Ensure that a directory exists.

    :param path: A directory path.
    """
    logger.debug('Making sure path exists: %s', path)
    try:
        os.makedirs(path)
        logger.debug(None, path)
    except OSError as exception:
        if exception.errno != errno.EEXIST:
            return False
    return True


def x_make_sure_path_exists__mutmut_10(path):
    """Ensure that a directory exists.

    :param path: A directory path.
    """
    logger.debug('Making sure path exists: %s', path)
    try:
        os.makedirs(path)
        logger.debug('Created directory at: %s', None)
    except OSError as exception:
        if exception.errno != errno.EEXIST:
            return False
    return True


def x_make_sure_path_exists__mutmut_11(path):
    """Ensure that a directory exists.

    :param path: A directory path.
    """
    logger.debug('Making sure path exists: %s', path)
    try:
        os.makedirs(path)
        logger.debug(path)
    except OSError as exception:
        if exception.errno != errno.EEXIST:
            return False
    return True


def x_make_sure_path_exists__mutmut_12(path):
    """Ensure that a directory exists.

    :param path: A directory path.
    """
    logger.debug('Making sure path exists: %s', path)
    try:
        os.makedirs(path)
        logger.debug('Created directory at: %s', )
    except OSError as exception:
        if exception.errno != errno.EEXIST:
            return False
    return True


def x_make_sure_path_exists__mutmut_13(path):
    """Ensure that a directory exists.

    :param path: A directory path.
    """
    logger.debug('Making sure path exists: %s', path)
    try:
        os.makedirs(path)
        logger.debug('XXCreated directory at: %sXX', path)
    except OSError as exception:
        if exception.errno != errno.EEXIST:
            return False
    return True


def x_make_sure_path_exists__mutmut_14(path):
    """Ensure that a directory exists.

    :param path: A directory path.
    """
    logger.debug('Making sure path exists: %s', path)
    try:
        os.makedirs(path)
        logger.debug('created directory at: %s', path)
    except OSError as exception:
        if exception.errno != errno.EEXIST:
            return False
    return True


def x_make_sure_path_exists__mutmut_15(path):
    """Ensure that a directory exists.

    :param path: A directory path.
    """
    logger.debug('Making sure path exists: %s', path)
    try:
        os.makedirs(path)
        logger.debug('CREATED DIRECTORY AT: %S', path)
    except OSError as exception:
        if exception.errno != errno.EEXIST:
            return False
    return True


def x_make_sure_path_exists__mutmut_16(path):
    """Ensure that a directory exists.

    :param path: A directory path.
    """
    logger.debug('Making sure path exists: %s', path)
    try:
        os.makedirs(path)
        logger.debug('Created directory at: %s', path)
    except OSError as exception:
        if exception.errno == errno.EEXIST:
            return False
    return True


def x_make_sure_path_exists__mutmut_17(path):
    """Ensure that a directory exists.

    :param path: A directory path.
    """
    logger.debug('Making sure path exists: %s', path)
    try:
        os.makedirs(path)
        logger.debug('Created directory at: %s', path)
    except OSError as exception:
        if exception.errno != errno.EEXIST:
            return True
    return True


def x_make_sure_path_exists__mutmut_18(path):
    """Ensure that a directory exists.

    :param path: A directory path.
    """
    logger.debug('Making sure path exists: %s', path)
    try:
        os.makedirs(path)
        logger.debug('Created directory at: %s', path)
    except OSError as exception:
        if exception.errno != errno.EEXIST:
            return False
    return False

x_make_sure_path_exists__mutmut_mutants : ClassVar[MutantDict] = { # type: ignore
'x_make_sure_path_exists__mutmut_1': x_make_sure_path_exists__mutmut_1, 
    'x_make_sure_path_exists__mutmut_2': x_make_sure_path_exists__mutmut_2, 
    'x_make_sure_path_exists__mutmut_3': x_make_sure_path_exists__mutmut_3, 
    'x_make_sure_path_exists__mutmut_4': x_make_sure_path_exists__mutmut_4, 
    'x_make_sure_path_exists__mutmut_5': x_make_sure_path_exists__mutmut_5, 
    'x_make_sure_path_exists__mutmut_6': x_make_sure_path_exists__mutmut_6, 
    'x_make_sure_path_exists__mutmut_7': x_make_sure_path_exists__mutmut_7, 
    'x_make_sure_path_exists__mutmut_8': x_make_sure_path_exists__mutmut_8, 
    'x_make_sure_path_exists__mutmut_9': x_make_sure_path_exists__mutmut_9, 
    'x_make_sure_path_exists__mutmut_10': x_make_sure_path_exists__mutmut_10, 
    'x_make_sure_path_exists__mutmut_11': x_make_sure_path_exists__mutmut_11, 
    'x_make_sure_path_exists__mutmut_12': x_make_sure_path_exists__mutmut_12, 
    'x_make_sure_path_exists__mutmut_13': x_make_sure_path_exists__mutmut_13, 
    'x_make_sure_path_exists__mutmut_14': x_make_sure_path_exists__mutmut_14, 
    'x_make_sure_path_exists__mutmut_15': x_make_sure_path_exists__mutmut_15, 
    'x_make_sure_path_exists__mutmut_16': x_make_sure_path_exists__mutmut_16, 
    'x_make_sure_path_exists__mutmut_17': x_make_sure_path_exists__mutmut_17, 
    'x_make_sure_path_exists__mutmut_18': x_make_sure_path_exists__mutmut_18
}
x_make_sure_path_exists__mutmut_orig.__name__ = 'x_make_sure_path_exists'


@contextlib.contextmanager
def work_in(dirname=None):
    """Context manager version of os.chdir.

    When exited, returns to the working directory prior to entering.
    """
    curdir = os.getcwd()
    try:
        if dirname is not None:
            os.chdir(dirname)
        yield
    finally:
        os.chdir(curdir)


def make_executable(script_path):
    args = [script_path]# type: ignore
    kwargs = {}# type: ignore
    return _mutmut_trampoline(x_make_executable__mutmut_orig, x_make_executable__mutmut_mutants, args, kwargs, None)


def x_make_executable__mutmut_orig(script_path):
    """Make `script_path` executable.

    :param script_path: The file to change
    """
    status = os.stat(script_path)
    os.chmod(script_path, status.st_mode | stat.S_IEXEC)


def x_make_executable__mutmut_1(script_path):
    """Make `script_path` executable.

    :param script_path: The file to change
    """
    status = None
    os.chmod(script_path, status.st_mode | stat.S_IEXEC)


def x_make_executable__mutmut_2(script_path):
    """Make `script_path` executable.

    :param script_path: The file to change
    """
    status = os.stat(None)
    os.chmod(script_path, status.st_mode | stat.S_IEXEC)


def x_make_executable__mutmut_3(script_path):
    """Make `script_path` executable.

    :param script_path: The file to change
    """
    status = os.stat(script_path)
    os.chmod(None, status.st_mode | stat.S_IEXEC)


def x_make_executable__mutmut_4(script_path):
    """Make `script_path` executable.

    :param script_path: The file to change
    """
    status = os.stat(script_path)
    os.chmod(script_path, None)


def x_make_executable__mutmut_5(script_path):
    """Make `script_path` executable.

    :param script_path: The file to change
    """
    status = os.stat(script_path)
    os.chmod(status.st_mode | stat.S_IEXEC)


def x_make_executable__mutmut_6(script_path):
    """Make `script_path` executable.

    :param script_path: The file to change
    """
    status = os.stat(script_path)
    os.chmod(script_path, )


def x_make_executable__mutmut_7(script_path):
    """Make `script_path` executable.

    :param script_path: The file to change
    """
    status = os.stat(script_path)
    os.chmod(script_path, status.st_mode & stat.S_IEXEC)

x_make_executable__mutmut_mutants : ClassVar[MutantDict] = { # type: ignore
'x_make_executable__mutmut_1': x_make_executable__mutmut_1, 
    'x_make_executable__mutmut_2': x_make_executable__mutmut_2, 
    'x_make_executable__mutmut_3': x_make_executable__mutmut_3, 
    'x_make_executable__mutmut_4': x_make_executable__mutmut_4, 
    'x_make_executable__mutmut_5': x_make_executable__mutmut_5, 
    'x_make_executable__mutmut_6': x_make_executable__mutmut_6, 
    'x_make_executable__mutmut_7': x_make_executable__mutmut_7
}
x_make_executable__mutmut_orig.__name__ = 'x_make_executable'


def prompt_and_delete(path, no_input=False):
    args = [path, no_input]# type: ignore
    kwargs = {}# type: ignore
    return _mutmut_trampoline(x_prompt_and_delete__mutmut_orig, x_prompt_and_delete__mutmut_mutants, args, kwargs, None)


def x_prompt_and_delete__mutmut_orig(path, no_input=False):
    """
    Ask user if it's okay to delete the previously-downloaded file/directory.

    If yes, delete it. If no, checks to see if the old version should be
    reused. If yes, it's reused; otherwise, Cookiecutter exits.

    :param path: Previously downloaded zipfile.
    :param no_input: Suppress prompt to delete repo and just delete it.
    :return: True if the content was deleted
    """
    # Suppress prompt if called via API
    if no_input:
        ok_to_delete = True
    else:
        question = (
            "You've downloaded {} before. Is it okay to delete and re-download it?"
        ).format(path)

        ok_to_delete = read_user_yes_no(question, 'yes')

    if ok_to_delete:
        if os.path.isdir(path):
            rmtree(path)
        else:
            os.remove(path)
        return True
    else:
        ok_to_reuse = read_user_yes_no(
            "Do you want to re-use the existing version?", 'yes'
        )

        if ok_to_reuse:
            return False

        sys.exit()


def x_prompt_and_delete__mutmut_1(path, no_input=True):
    """
    Ask user if it's okay to delete the previously-downloaded file/directory.

    If yes, delete it. If no, checks to see if the old version should be
    reused. If yes, it's reused; otherwise, Cookiecutter exits.

    :param path: Previously downloaded zipfile.
    :param no_input: Suppress prompt to delete repo and just delete it.
    :return: True if the content was deleted
    """
    # Suppress prompt if called via API
    if no_input:
        ok_to_delete = True
    else:
        question = (
            "You've downloaded {} before. Is it okay to delete and re-download it?"
        ).format(path)

        ok_to_delete = read_user_yes_no(question, 'yes')

    if ok_to_delete:
        if os.path.isdir(path):
            rmtree(path)
        else:
            os.remove(path)
        return True
    else:
        ok_to_reuse = read_user_yes_no(
            "Do you want to re-use the existing version?", 'yes'
        )

        if ok_to_reuse:
            return False

        sys.exit()


def x_prompt_and_delete__mutmut_2(path, no_input=False):
    """
    Ask user if it's okay to delete the previously-downloaded file/directory.

    If yes, delete it. If no, checks to see if the old version should be
    reused. If yes, it's reused; otherwise, Cookiecutter exits.

    :param path: Previously downloaded zipfile.
    :param no_input: Suppress prompt to delete repo and just delete it.
    :return: True if the content was deleted
    """
    # Suppress prompt if called via API
    if no_input:
        ok_to_delete = None
    else:
        question = (
            "You've downloaded {} before. Is it okay to delete and re-download it?"
        ).format(path)

        ok_to_delete = read_user_yes_no(question, 'yes')

    if ok_to_delete:
        if os.path.isdir(path):
            rmtree(path)
        else:
            os.remove(path)
        return True
    else:
        ok_to_reuse = read_user_yes_no(
            "Do you want to re-use the existing version?", 'yes'
        )

        if ok_to_reuse:
            return False

        sys.exit()


def x_prompt_and_delete__mutmut_3(path, no_input=False):
    """
    Ask user if it's okay to delete the previously-downloaded file/directory.

    If yes, delete it. If no, checks to see if the old version should be
    reused. If yes, it's reused; otherwise, Cookiecutter exits.

    :param path: Previously downloaded zipfile.
    :param no_input: Suppress prompt to delete repo and just delete it.
    :return: True if the content was deleted
    """
    # Suppress prompt if called via API
    if no_input:
        ok_to_delete = False
    else:
        question = (
            "You've downloaded {} before. Is it okay to delete and re-download it?"
        ).format(path)

        ok_to_delete = read_user_yes_no(question, 'yes')

    if ok_to_delete:
        if os.path.isdir(path):
            rmtree(path)
        else:
            os.remove(path)
        return True
    else:
        ok_to_reuse = read_user_yes_no(
            "Do you want to re-use the existing version?", 'yes'
        )

        if ok_to_reuse:
            return False

        sys.exit()


def x_prompt_and_delete__mutmut_4(path, no_input=False):
    """
    Ask user if it's okay to delete the previously-downloaded file/directory.

    If yes, delete it. If no, checks to see if the old version should be
    reused. If yes, it's reused; otherwise, Cookiecutter exits.

    :param path: Previously downloaded zipfile.
    :param no_input: Suppress prompt to delete repo and just delete it.
    :return: True if the content was deleted
    """
    # Suppress prompt if called via API
    if no_input:
        ok_to_delete = True
    else:
        question = None

        ok_to_delete = read_user_yes_no(question, 'yes')

    if ok_to_delete:
        if os.path.isdir(path):
            rmtree(path)
        else:
            os.remove(path)
        return True
    else:
        ok_to_reuse = read_user_yes_no(
            "Do you want to re-use the existing version?", 'yes'
        )

        if ok_to_reuse:
            return False

        sys.exit()


def x_prompt_and_delete__mutmut_5(path, no_input=False):
    """
    Ask user if it's okay to delete the previously-downloaded file/directory.

    If yes, delete it. If no, checks to see if the old version should be
    reused. If yes, it's reused; otherwise, Cookiecutter exits.

    :param path: Previously downloaded zipfile.
    :param no_input: Suppress prompt to delete repo and just delete it.
    :return: True if the content was deleted
    """
    # Suppress prompt if called via API
    if no_input:
        ok_to_delete = True
    else:
        question = (
            "You've downloaded {} before. Is it okay to delete and re-download it?"
        ).format(None)

        ok_to_delete = read_user_yes_no(question, 'yes')

    if ok_to_delete:
        if os.path.isdir(path):
            rmtree(path)
        else:
            os.remove(path)
        return True
    else:
        ok_to_reuse = read_user_yes_no(
            "Do you want to re-use the existing version?", 'yes'
        )

        if ok_to_reuse:
            return False

        sys.exit()


def x_prompt_and_delete__mutmut_6(path, no_input=False):
    """
    Ask user if it's okay to delete the previously-downloaded file/directory.

    If yes, delete it. If no, checks to see if the old version should be
    reused. If yes, it's reused; otherwise, Cookiecutter exits.

    :param path: Previously downloaded zipfile.
    :param no_input: Suppress prompt to delete repo and just delete it.
    :return: True if the content was deleted
    """
    # Suppress prompt if called via API
    if no_input:
        ok_to_delete = True
    else:
        question = (
            "XXYou've downloaded {} before. Is it okay to delete and re-download it?XX"
        ).format(path)

        ok_to_delete = read_user_yes_no(question, 'yes')

    if ok_to_delete:
        if os.path.isdir(path):
            rmtree(path)
        else:
            os.remove(path)
        return True
    else:
        ok_to_reuse = read_user_yes_no(
            "Do you want to re-use the existing version?", 'yes'
        )

        if ok_to_reuse:
            return False

        sys.exit()


def x_prompt_and_delete__mutmut_7(path, no_input=False):
    """
    Ask user if it's okay to delete the previously-downloaded file/directory.

    If yes, delete it. If no, checks to see if the old version should be
    reused. If yes, it's reused; otherwise, Cookiecutter exits.

    :param path: Previously downloaded zipfile.
    :param no_input: Suppress prompt to delete repo and just delete it.
    :return: True if the content was deleted
    """
    # Suppress prompt if called via API
    if no_input:
        ok_to_delete = True
    else:
        question = (
            "you've downloaded {} before. is it okay to delete and re-download it?"
        ).format(path)

        ok_to_delete = read_user_yes_no(question, 'yes')

    if ok_to_delete:
        if os.path.isdir(path):
            rmtree(path)
        else:
            os.remove(path)
        return True
    else:
        ok_to_reuse = read_user_yes_no(
            "Do you want to re-use the existing version?", 'yes'
        )

        if ok_to_reuse:
            return False

        sys.exit()


def x_prompt_and_delete__mutmut_8(path, no_input=False):
    """
    Ask user if it's okay to delete the previously-downloaded file/directory.

    If yes, delete it. If no, checks to see if the old version should be
    reused. If yes, it's reused; otherwise, Cookiecutter exits.

    :param path: Previously downloaded zipfile.
    :param no_input: Suppress prompt to delete repo and just delete it.
    :return: True if the content was deleted
    """
    # Suppress prompt if called via API
    if no_input:
        ok_to_delete = True
    else:
        question = (
            "YOU'VE DOWNLOADED {} BEFORE. IS IT OKAY TO DELETE AND RE-DOWNLOAD IT?"
        ).format(path)

        ok_to_delete = read_user_yes_no(question, 'yes')

    if ok_to_delete:
        if os.path.isdir(path):
            rmtree(path)
        else:
            os.remove(path)
        return True
    else:
        ok_to_reuse = read_user_yes_no(
            "Do you want to re-use the existing version?", 'yes'
        )

        if ok_to_reuse:
            return False

        sys.exit()


def x_prompt_and_delete__mutmut_9(path, no_input=False):
    """
    Ask user if it's okay to delete the previously-downloaded file/directory.

    If yes, delete it. If no, checks to see if the old version should be
    reused. If yes, it's reused; otherwise, Cookiecutter exits.

    :param path: Previously downloaded zipfile.
    :param no_input: Suppress prompt to delete repo and just delete it.
    :return: True if the content was deleted
    """
    # Suppress prompt if called via API
    if no_input:
        ok_to_delete = True
    else:
        question = (
            "You've downloaded {} before. Is it okay to delete and re-download it?"
        ).format(path)

        ok_to_delete = None

    if ok_to_delete:
        if os.path.isdir(path):
            rmtree(path)
        else:
            os.remove(path)
        return True
    else:
        ok_to_reuse = read_user_yes_no(
            "Do you want to re-use the existing version?", 'yes'
        )

        if ok_to_reuse:
            return False

        sys.exit()


def x_prompt_and_delete__mutmut_10(path, no_input=False):
    """
    Ask user if it's okay to delete the previously-downloaded file/directory.

    If yes, delete it. If no, checks to see if the old version should be
    reused. If yes, it's reused; otherwise, Cookiecutter exits.

    :param path: Previously downloaded zipfile.
    :param no_input: Suppress prompt to delete repo and just delete it.
    :return: True if the content was deleted
    """
    # Suppress prompt if called via API
    if no_input:
        ok_to_delete = True
    else:
        question = (
            "You've downloaded {} before. Is it okay to delete and re-download it?"
        ).format(path)

        ok_to_delete = read_user_yes_no(None, 'yes')

    if ok_to_delete:
        if os.path.isdir(path):
            rmtree(path)
        else:
            os.remove(path)
        return True
    else:
        ok_to_reuse = read_user_yes_no(
            "Do you want to re-use the existing version?", 'yes'
        )

        if ok_to_reuse:
            return False

        sys.exit()


def x_prompt_and_delete__mutmut_11(path, no_input=False):
    """
    Ask user if it's okay to delete the previously-downloaded file/directory.

    If yes, delete it. If no, checks to see if the old version should be
    reused. If yes, it's reused; otherwise, Cookiecutter exits.

    :param path: Previously downloaded zipfile.
    :param no_input: Suppress prompt to delete repo and just delete it.
    :return: True if the content was deleted
    """
    # Suppress prompt if called via API
    if no_input:
        ok_to_delete = True
    else:
        question = (
            "You've downloaded {} before. Is it okay to delete and re-download it?"
        ).format(path)

        ok_to_delete = read_user_yes_no(question, None)

    if ok_to_delete:
        if os.path.isdir(path):
            rmtree(path)
        else:
            os.remove(path)
        return True
    else:
        ok_to_reuse = read_user_yes_no(
            "Do you want to re-use the existing version?", 'yes'
        )

        if ok_to_reuse:
            return False

        sys.exit()


def x_prompt_and_delete__mutmut_12(path, no_input=False):
    """
    Ask user if it's okay to delete the previously-downloaded file/directory.

    If yes, delete it. If no, checks to see if the old version should be
    reused. If yes, it's reused; otherwise, Cookiecutter exits.

    :param path: Previously downloaded zipfile.
    :param no_input: Suppress prompt to delete repo and just delete it.
    :return: True if the content was deleted
    """
    # Suppress prompt if called via API
    if no_input:
        ok_to_delete = True
    else:
        question = (
            "You've downloaded {} before. Is it okay to delete and re-download it?"
        ).format(path)

        ok_to_delete = read_user_yes_no('yes')

    if ok_to_delete:
        if os.path.isdir(path):
            rmtree(path)
        else:
            os.remove(path)
        return True
    else:
        ok_to_reuse = read_user_yes_no(
            "Do you want to re-use the existing version?", 'yes'
        )

        if ok_to_reuse:
            return False

        sys.exit()


def x_prompt_and_delete__mutmut_13(path, no_input=False):
    """
    Ask user if it's okay to delete the previously-downloaded file/directory.

    If yes, delete it. If no, checks to see if the old version should be
    reused. If yes, it's reused; otherwise, Cookiecutter exits.

    :param path: Previously downloaded zipfile.
    :param no_input: Suppress prompt to delete repo and just delete it.
    :return: True if the content was deleted
    """
    # Suppress prompt if called via API
    if no_input:
        ok_to_delete = True
    else:
        question = (
            "You've downloaded {} before. Is it okay to delete and re-download it?"
        ).format(path)

        ok_to_delete = read_user_yes_no(question, )

    if ok_to_delete:
        if os.path.isdir(path):
            rmtree(path)
        else:
            os.remove(path)
        return True
    else:
        ok_to_reuse = read_user_yes_no(
            "Do you want to re-use the existing version?", 'yes'
        )

        if ok_to_reuse:
            return False

        sys.exit()


def x_prompt_and_delete__mutmut_14(path, no_input=False):
    """
    Ask user if it's okay to delete the previously-downloaded file/directory.

    If yes, delete it. If no, checks to see if the old version should be
    reused. If yes, it's reused; otherwise, Cookiecutter exits.

    :param path: Previously downloaded zipfile.
    :param no_input: Suppress prompt to delete repo and just delete it.
    :return: True if the content was deleted
    """
    # Suppress prompt if called via API
    if no_input:
        ok_to_delete = True
    else:
        question = (
            "You've downloaded {} before. Is it okay to delete and re-download it?"
        ).format(path)

        ok_to_delete = read_user_yes_no(question, 'XXyesXX')

    if ok_to_delete:
        if os.path.isdir(path):
            rmtree(path)
        else:
            os.remove(path)
        return True
    else:
        ok_to_reuse = read_user_yes_no(
            "Do you want to re-use the existing version?", 'yes'
        )

        if ok_to_reuse:
            return False

        sys.exit()


def x_prompt_and_delete__mutmut_15(path, no_input=False):
    """
    Ask user if it's okay to delete the previously-downloaded file/directory.

    If yes, delete it. If no, checks to see if the old version should be
    reused. If yes, it's reused; otherwise, Cookiecutter exits.

    :param path: Previously downloaded zipfile.
    :param no_input: Suppress prompt to delete repo and just delete it.
    :return: True if the content was deleted
    """
    # Suppress prompt if called via API
    if no_input:
        ok_to_delete = True
    else:
        question = (
            "You've downloaded {} before. Is it okay to delete and re-download it?"
        ).format(path)

        ok_to_delete = read_user_yes_no(question, 'YES')

    if ok_to_delete:
        if os.path.isdir(path):
            rmtree(path)
        else:
            os.remove(path)
        return True
    else:
        ok_to_reuse = read_user_yes_no(
            "Do you want to re-use the existing version?", 'yes'
        )

        if ok_to_reuse:
            return False

        sys.exit()


def x_prompt_and_delete__mutmut_16(path, no_input=False):
    """
    Ask user if it's okay to delete the previously-downloaded file/directory.

    If yes, delete it. If no, checks to see if the old version should be
    reused. If yes, it's reused; otherwise, Cookiecutter exits.

    :param path: Previously downloaded zipfile.
    :param no_input: Suppress prompt to delete repo and just delete it.
    :return: True if the content was deleted
    """
    # Suppress prompt if called via API
    if no_input:
        ok_to_delete = True
    else:
        question = (
            "You've downloaded {} before. Is it okay to delete and re-download it?"
        ).format(path)

        ok_to_delete = read_user_yes_no(question, 'yes')

    if ok_to_delete:
        if os.path.isdir(None):
            rmtree(path)
        else:
            os.remove(path)
        return True
    else:
        ok_to_reuse = read_user_yes_no(
            "Do you want to re-use the existing version?", 'yes'
        )

        if ok_to_reuse:
            return False

        sys.exit()


def x_prompt_and_delete__mutmut_17(path, no_input=False):
    """
    Ask user if it's okay to delete the previously-downloaded file/directory.

    If yes, delete it. If no, checks to see if the old version should be
    reused. If yes, it's reused; otherwise, Cookiecutter exits.

    :param path: Previously downloaded zipfile.
    :param no_input: Suppress prompt to delete repo and just delete it.
    :return: True if the content was deleted
    """
    # Suppress prompt if called via API
    if no_input:
        ok_to_delete = True
    else:
        question = (
            "You've downloaded {} before. Is it okay to delete and re-download it?"
        ).format(path)

        ok_to_delete = read_user_yes_no(question, 'yes')

    if ok_to_delete:
        if os.path.isdir(path):
            rmtree(None)
        else:
            os.remove(path)
        return True
    else:
        ok_to_reuse = read_user_yes_no(
            "Do you want to re-use the existing version?", 'yes'
        )

        if ok_to_reuse:
            return False

        sys.exit()


def x_prompt_and_delete__mutmut_18(path, no_input=False):
    """
    Ask user if it's okay to delete the previously-downloaded file/directory.

    If yes, delete it. If no, checks to see if the old version should be
    reused. If yes, it's reused; otherwise, Cookiecutter exits.

    :param path: Previously downloaded zipfile.
    :param no_input: Suppress prompt to delete repo and just delete it.
    :return: True if the content was deleted
    """
    # Suppress prompt if called via API
    if no_input:
        ok_to_delete = True
    else:
        question = (
            "You've downloaded {} before. Is it okay to delete and re-download it?"
        ).format(path)

        ok_to_delete = read_user_yes_no(question, 'yes')

    if ok_to_delete:
        if os.path.isdir(path):
            rmtree(path)
        else:
            os.remove(None)
        return True
    else:
        ok_to_reuse = read_user_yes_no(
            "Do you want to re-use the existing version?", 'yes'
        )

        if ok_to_reuse:
            return False

        sys.exit()


def x_prompt_and_delete__mutmut_19(path, no_input=False):
    """
    Ask user if it's okay to delete the previously-downloaded file/directory.

    If yes, delete it. If no, checks to see if the old version should be
    reused. If yes, it's reused; otherwise, Cookiecutter exits.

    :param path: Previously downloaded zipfile.
    :param no_input: Suppress prompt to delete repo and just delete it.
    :return: True if the content was deleted
    """
    # Suppress prompt if called via API
    if no_input:
        ok_to_delete = True
    else:
        question = (
            "You've downloaded {} before. Is it okay to delete and re-download it?"
        ).format(path)

        ok_to_delete = read_user_yes_no(question, 'yes')

    if ok_to_delete:
        if os.path.isdir(path):
            rmtree(path)
        else:
            os.remove(path)
        return False
    else:
        ok_to_reuse = read_user_yes_no(
            "Do you want to re-use the existing version?", 'yes'
        )

        if ok_to_reuse:
            return False

        sys.exit()


def x_prompt_and_delete__mutmut_20(path, no_input=False):
    """
    Ask user if it's okay to delete the previously-downloaded file/directory.

    If yes, delete it. If no, checks to see if the old version should be
    reused. If yes, it's reused; otherwise, Cookiecutter exits.

    :param path: Previously downloaded zipfile.
    :param no_input: Suppress prompt to delete repo and just delete it.
    :return: True if the content was deleted
    """
    # Suppress prompt if called via API
    if no_input:
        ok_to_delete = True
    else:
        question = (
            "You've downloaded {} before. Is it okay to delete and re-download it?"
        ).format(path)

        ok_to_delete = read_user_yes_no(question, 'yes')

    if ok_to_delete:
        if os.path.isdir(path):
            rmtree(path)
        else:
            os.remove(path)
        return True
    else:
        ok_to_reuse = None

        if ok_to_reuse:
            return False

        sys.exit()


def x_prompt_and_delete__mutmut_21(path, no_input=False):
    """
    Ask user if it's okay to delete the previously-downloaded file/directory.

    If yes, delete it. If no, checks to see if the old version should be
    reused. If yes, it's reused; otherwise, Cookiecutter exits.

    :param path: Previously downloaded zipfile.
    :param no_input: Suppress prompt to delete repo and just delete it.
    :return: True if the content was deleted
    """
    # Suppress prompt if called via API
    if no_input:
        ok_to_delete = True
    else:
        question = (
            "You've downloaded {} before. Is it okay to delete and re-download it?"
        ).format(path)

        ok_to_delete = read_user_yes_no(question, 'yes')

    if ok_to_delete:
        if os.path.isdir(path):
            rmtree(path)
        else:
            os.remove(path)
        return True
    else:
        ok_to_reuse = read_user_yes_no(
            None, 'yes'
        )

        if ok_to_reuse:
            return False

        sys.exit()


def x_prompt_and_delete__mutmut_22(path, no_input=False):
    """
    Ask user if it's okay to delete the previously-downloaded file/directory.

    If yes, delete it. If no, checks to see if the old version should be
    reused. If yes, it's reused; otherwise, Cookiecutter exits.

    :param path: Previously downloaded zipfile.
    :param no_input: Suppress prompt to delete repo and just delete it.
    :return: True if the content was deleted
    """
    # Suppress prompt if called via API
    if no_input:
        ok_to_delete = True
    else:
        question = (
            "You've downloaded {} before. Is it okay to delete and re-download it?"
        ).format(path)

        ok_to_delete = read_user_yes_no(question, 'yes')

    if ok_to_delete:
        if os.path.isdir(path):
            rmtree(path)
        else:
            os.remove(path)
        return True
    else:
        ok_to_reuse = read_user_yes_no(
            "Do you want to re-use the existing version?", None
        )

        if ok_to_reuse:
            return False

        sys.exit()


def x_prompt_and_delete__mutmut_23(path, no_input=False):
    """
    Ask user if it's okay to delete the previously-downloaded file/directory.

    If yes, delete it. If no, checks to see if the old version should be
    reused. If yes, it's reused; otherwise, Cookiecutter exits.

    :param path: Previously downloaded zipfile.
    :param no_input: Suppress prompt to delete repo and just delete it.
    :return: True if the content was deleted
    """
    # Suppress prompt if called via API
    if no_input:
        ok_to_delete = True
    else:
        question = (
            "You've downloaded {} before. Is it okay to delete and re-download it?"
        ).format(path)

        ok_to_delete = read_user_yes_no(question, 'yes')

    if ok_to_delete:
        if os.path.isdir(path):
            rmtree(path)
        else:
            os.remove(path)
        return True
    else:
        ok_to_reuse = read_user_yes_no(
            'yes'
        )

        if ok_to_reuse:
            return False

        sys.exit()


def x_prompt_and_delete__mutmut_24(path, no_input=False):
    """
    Ask user if it's okay to delete the previously-downloaded file/directory.

    If yes, delete it. If no, checks to see if the old version should be
    reused. If yes, it's reused; otherwise, Cookiecutter exits.

    :param path: Previously downloaded zipfile.
    :param no_input: Suppress prompt to delete repo and just delete it.
    :return: True if the content was deleted
    """
    # Suppress prompt if called via API
    if no_input:
        ok_to_delete = True
    else:
        question = (
            "You've downloaded {} before. Is it okay to delete and re-download it?"
        ).format(path)

        ok_to_delete = read_user_yes_no(question, 'yes')

    if ok_to_delete:
        if os.path.isdir(path):
            rmtree(path)
        else:
            os.remove(path)
        return True
    else:
        ok_to_reuse = read_user_yes_no(
            "Do you want to re-use the existing version?", )

        if ok_to_reuse:
            return False

        sys.exit()


def x_prompt_and_delete__mutmut_25(path, no_input=False):
    """
    Ask user if it's okay to delete the previously-downloaded file/directory.

    If yes, delete it. If no, checks to see if the old version should be
    reused. If yes, it's reused; otherwise, Cookiecutter exits.

    :param path: Previously downloaded zipfile.
    :param no_input: Suppress prompt to delete repo and just delete it.
    :return: True if the content was deleted
    """
    # Suppress prompt if called via API
    if no_input:
        ok_to_delete = True
    else:
        question = (
            "You've downloaded {} before. Is it okay to delete and re-download it?"
        ).format(path)

        ok_to_delete = read_user_yes_no(question, 'yes')

    if ok_to_delete:
        if os.path.isdir(path):
            rmtree(path)
        else:
            os.remove(path)
        return True
    else:
        ok_to_reuse = read_user_yes_no(
            "XXDo you want to re-use the existing version?XX", 'yes'
        )

        if ok_to_reuse:
            return False

        sys.exit()


def x_prompt_and_delete__mutmut_26(path, no_input=False):
    """
    Ask user if it's okay to delete the previously-downloaded file/directory.

    If yes, delete it. If no, checks to see if the old version should be
    reused. If yes, it's reused; otherwise, Cookiecutter exits.

    :param path: Previously downloaded zipfile.
    :param no_input: Suppress prompt to delete repo and just delete it.
    :return: True if the content was deleted
    """
    # Suppress prompt if called via API
    if no_input:
        ok_to_delete = True
    else:
        question = (
            "You've downloaded {} before. Is it okay to delete and re-download it?"
        ).format(path)

        ok_to_delete = read_user_yes_no(question, 'yes')

    if ok_to_delete:
        if os.path.isdir(path):
            rmtree(path)
        else:
            os.remove(path)
        return True
    else:
        ok_to_reuse = read_user_yes_no(
            "do you want to re-use the existing version?", 'yes'
        )

        if ok_to_reuse:
            return False

        sys.exit()


def x_prompt_and_delete__mutmut_27(path, no_input=False):
    """
    Ask user if it's okay to delete the previously-downloaded file/directory.

    If yes, delete it. If no, checks to see if the old version should be
    reused. If yes, it's reused; otherwise, Cookiecutter exits.

    :param path: Previously downloaded zipfile.
    :param no_input: Suppress prompt to delete repo and just delete it.
    :return: True if the content was deleted
    """
    # Suppress prompt if called via API
    if no_input:
        ok_to_delete = True
    else:
        question = (
            "You've downloaded {} before. Is it okay to delete and re-download it?"
        ).format(path)

        ok_to_delete = read_user_yes_no(question, 'yes')

    if ok_to_delete:
        if os.path.isdir(path):
            rmtree(path)
        else:
            os.remove(path)
        return True
    else:
        ok_to_reuse = read_user_yes_no(
            "DO YOU WANT TO RE-USE THE EXISTING VERSION?", 'yes'
        )

        if ok_to_reuse:
            return False

        sys.exit()


def x_prompt_and_delete__mutmut_28(path, no_input=False):
    """
    Ask user if it's okay to delete the previously-downloaded file/directory.

    If yes, delete it. If no, checks to see if the old version should be
    reused. If yes, it's reused; otherwise, Cookiecutter exits.

    :param path: Previously downloaded zipfile.
    :param no_input: Suppress prompt to delete repo and just delete it.
    :return: True if the content was deleted
    """
    # Suppress prompt if called via API
    if no_input:
        ok_to_delete = True
    else:
        question = (
            "You've downloaded {} before. Is it okay to delete and re-download it?"
        ).format(path)

        ok_to_delete = read_user_yes_no(question, 'yes')

    if ok_to_delete:
        if os.path.isdir(path):
            rmtree(path)
        else:
            os.remove(path)
        return True
    else:
        ok_to_reuse = read_user_yes_no(
            "Do you want to re-use the existing version?", 'XXyesXX'
        )

        if ok_to_reuse:
            return False

        sys.exit()


def x_prompt_and_delete__mutmut_29(path, no_input=False):
    """
    Ask user if it's okay to delete the previously-downloaded file/directory.

    If yes, delete it. If no, checks to see if the old version should be
    reused. If yes, it's reused; otherwise, Cookiecutter exits.

    :param path: Previously downloaded zipfile.
    :param no_input: Suppress prompt to delete repo and just delete it.
    :return: True if the content was deleted
    """
    # Suppress prompt if called via API
    if no_input:
        ok_to_delete = True
    else:
        question = (
            "You've downloaded {} before. Is it okay to delete and re-download it?"
        ).format(path)

        ok_to_delete = read_user_yes_no(question, 'yes')

    if ok_to_delete:
        if os.path.isdir(path):
            rmtree(path)
        else:
            os.remove(path)
        return True
    else:
        ok_to_reuse = read_user_yes_no(
            "Do you want to re-use the existing version?", 'YES'
        )

        if ok_to_reuse:
            return False

        sys.exit()


def x_prompt_and_delete__mutmut_30(path, no_input=False):
    """
    Ask user if it's okay to delete the previously-downloaded file/directory.

    If yes, delete it. If no, checks to see if the old version should be
    reused. If yes, it's reused; otherwise, Cookiecutter exits.

    :param path: Previously downloaded zipfile.
    :param no_input: Suppress prompt to delete repo and just delete it.
    :return: True if the content was deleted
    """
    # Suppress prompt if called via API
    if no_input:
        ok_to_delete = True
    else:
        question = (
            "You've downloaded {} before. Is it okay to delete and re-download it?"
        ).format(path)

        ok_to_delete = read_user_yes_no(question, 'yes')

    if ok_to_delete:
        if os.path.isdir(path):
            rmtree(path)
        else:
            os.remove(path)
        return True
    else:
        ok_to_reuse = read_user_yes_no(
            "Do you want to re-use the existing version?", 'yes'
        )

        if ok_to_reuse:
            return True

        sys.exit()

x_prompt_and_delete__mutmut_mutants : ClassVar[MutantDict] = { # type: ignore
'x_prompt_and_delete__mutmut_1': x_prompt_and_delete__mutmut_1, 
    'x_prompt_and_delete__mutmut_2': x_prompt_and_delete__mutmut_2, 
    'x_prompt_and_delete__mutmut_3': x_prompt_and_delete__mutmut_3, 
    'x_prompt_and_delete__mutmut_4': x_prompt_and_delete__mutmut_4, 
    'x_prompt_and_delete__mutmut_5': x_prompt_and_delete__mutmut_5, 
    'x_prompt_and_delete__mutmut_6': x_prompt_and_delete__mutmut_6, 
    'x_prompt_and_delete__mutmut_7': x_prompt_and_delete__mutmut_7, 
    'x_prompt_and_delete__mutmut_8': x_prompt_and_delete__mutmut_8, 
    'x_prompt_and_delete__mutmut_9': x_prompt_and_delete__mutmut_9, 
    'x_prompt_and_delete__mutmut_10': x_prompt_and_delete__mutmut_10, 
    'x_prompt_and_delete__mutmut_11': x_prompt_and_delete__mutmut_11, 
    'x_prompt_and_delete__mutmut_12': x_prompt_and_delete__mutmut_12, 
    'x_prompt_and_delete__mutmut_13': x_prompt_and_delete__mutmut_13, 
    'x_prompt_and_delete__mutmut_14': x_prompt_and_delete__mutmut_14, 
    'x_prompt_and_delete__mutmut_15': x_prompt_and_delete__mutmut_15, 
    'x_prompt_and_delete__mutmut_16': x_prompt_and_delete__mutmut_16, 
    'x_prompt_and_delete__mutmut_17': x_prompt_and_delete__mutmut_17, 
    'x_prompt_and_delete__mutmut_18': x_prompt_and_delete__mutmut_18, 
    'x_prompt_and_delete__mutmut_19': x_prompt_and_delete__mutmut_19, 
    'x_prompt_and_delete__mutmut_20': x_prompt_and_delete__mutmut_20, 
    'x_prompt_and_delete__mutmut_21': x_prompt_and_delete__mutmut_21, 
    'x_prompt_and_delete__mutmut_22': x_prompt_and_delete__mutmut_22, 
    'x_prompt_and_delete__mutmut_23': x_prompt_and_delete__mutmut_23, 
    'x_prompt_and_delete__mutmut_24': x_prompt_and_delete__mutmut_24, 
    'x_prompt_and_delete__mutmut_25': x_prompt_and_delete__mutmut_25, 
    'x_prompt_and_delete__mutmut_26': x_prompt_and_delete__mutmut_26, 
    'x_prompt_and_delete__mutmut_27': x_prompt_and_delete__mutmut_27, 
    'x_prompt_and_delete__mutmut_28': x_prompt_and_delete__mutmut_28, 
    'x_prompt_and_delete__mutmut_29': x_prompt_and_delete__mutmut_29, 
    'x_prompt_and_delete__mutmut_30': x_prompt_and_delete__mutmut_30
}
x_prompt_and_delete__mutmut_orig.__name__ = 'x_prompt_and_delete'
