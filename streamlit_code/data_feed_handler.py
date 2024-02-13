import sys
#sys.path.append('/h/git-projects/python-code/')
sys.path.append("H:\\git-projects\\python-code")
from pkg_common import mod_others as m_oth

def main():
  m_oth.logger.debug("main()")


# main
if __name__ == "__main__":
  print(sys.path)
  m_oth.fn_set_logger(True)

  main()

