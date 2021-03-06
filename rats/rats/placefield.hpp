#pragma once
#include "defs.hpp"
#include "path.hpp"
#include "placecell.hpp"
#include "../include/glm/glm.hpp"
#include <tuple>
#include "sprite.hpp"
#include "spritefamily.hpp"

class PlaceField {
private:
  const static int num_divisions = 25;
  std::vector<std::vector<int> > spike_counts;
  std::vector<std::vector<int> > visit_counts;

  SpriteFamily divisions;
  SpriteFamily place_fields;

public:
	PlaceField();
	std::tuple<int,int> getCoords(glm::vec2 location);
	std::vector<std::vector<float> > findMaxDivision(Path &path, PlaceCell &place_cell);
	void drawBoxes();
	void drawField();
};
