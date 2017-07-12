#pragma once

#include <deque>
#include "../include/glm/glm.hpp"
#include "defs.hpp"

class PlaceCell {
private:
  std::deque<GLfloat> times;
  std::deque<GLfloat>::iterator next_time;
  GLfloat *current_time;
  glm::vec4 colour;
  const char *spike_bin_filename;

public:
  PlaceCell(const char *filename, glm::vec4 colour, bool use_hmm, GLfloat start_time, GLfloat end_time, const char *output_filename);
  GLfloat *getNextTime();
  GLfloat *getCurrentTime();
  GLfloat *checkNextTime();
  glm::vec4 getColour();
  const char* getOutputFilename();
};
