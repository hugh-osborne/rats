#include <stdio.h>
#include <stdlib.h>
#include <fstream>
#include <cstdlib>
#include <string>
#include <sstream>
#include <vector>
#include <iterator>

class StringSplit {
public:
  template<typename Out>
  static void split(const std::string &s, char delim, Out result);

  static std::vector<std::string> split(const std::string &s, char delim);
};
