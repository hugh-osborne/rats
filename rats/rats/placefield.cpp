#include "placefield.hpp"
#include <stdio.h>
#include <stdlib.h>

PlaceField::PlaceField() {
	place_fields = SpriteFamily("blotch.bmp");
	divisions = SpriteFamily("division.bmp");
	for (int i = 0; i < num_divisions; i++) {
		std::vector<int> s;
		std::vector<int> v;
		for (int j = 0; j < num_divisions; j++) {
			s.push_back(0);
			v.push_back(0);
		}
		spike_counts.push_back(s);
		visit_counts.push_back(v);
	}
}

std::tuple<int,int> PlaceField::getCoords(glm::vec2 location) {
  GLfloat dim = 2.0f / num_divisions;
  int x = (location.x + 1.0f) / dim;
  int y = (location.y + 1.0f) / dim;

  if (x >= num_divisions) x = num_divisions - 1;
  if (x < 0) x = 0;
  if (y >= num_divisions) y = num_divisions - 1;
  if (y < 0) y = 0;

  return std::make_tuple(x, y);
}

std::tuple<int, int, float> PlaceField::findMaxDivision(Path &path, PlaceCell &place_cell) {
  PathPoint *pp = path.getNextPoint();
	place_cell.getNextTime();

	while (pp) {
    std::tuple<int,int> coord = getCoords(pp->position);

		if (place_cell.checkNextTime() && place_cell.getCurrentTime() && (pp->time > *(place_cell.getCurrentTime()))) {
			place_fields.addSprite(Sprite(pp->position, glm::vec2(0.1, 0.1), glm::vec4(1.0f,1.0f,1.0f,1.0f), 1.0f));
			spike_counts[std::get<0>(coord)][std::get<1>(coord)]++;
			place_cell.getNextTime();
		}

     visit_counts[std::get<0>(coord)][std::get<1>(coord)]++;
		pp = path.getNextPoint();
	}

  float max_spiking = 0.0f;
  std::tuple<int,int> max_spiking_coords = std::make_tuple(-1, -1);
  float total_likelihood = 0.0f;

  for(int i=0; i<num_divisions; i++) {
    for (int j=0; j<num_divisions; j++) {
      if(visit_counts[i][j] > 0) {
        float l = (GLfloat)((float)spike_counts[i][j]/(float)visit_counts[i][j]);
        if(l > max_spiking) {
          max_spiking = l;
          max_spiking_coords = std::make_tuple(i, j);
        }
        total_likelihood += l;
      }
    }
  }

  printf("Max Spike Likelihood : %f at [%i,%i]\n", max_spiking, std::get<0>(max_spiking_coords), std::get<1>(max_spiking_coords));

 GLfloat dim = 2.0f / num_divisions;
  for(int i=0; i<num_divisions; i++) {
    for (int j=0; j<num_divisions; j++) {
      float alpha = 0.0f;
      if(visit_counts[i][j] > 0 && total_likelihood > 0.0f) {
        alpha = (GLfloat)((float)spike_counts[i][j]/(float)visit_counts[i][j]) / total_likelihood;
      }
		divisions.addSprite(Sprite(glm::vec2((i*dim) - 1.0f + (dim / 2.0f), (j*dim) - 1.0f + (dim / 2.0f)), glm::vec2(dim / 2.0f, dim / 2.0f),
			glm::vec4(1.0f, 0.0f, 0.0f, alpha), 1.0f));
    }
  }

  return std::make_tuple(std::get<0>(max_spiking_coords), std::get<1>(max_spiking_coords), max_spiking);
}

void PlaceField::drawBoxes() {
  divisions.draw();
}

void PlaceField::drawField() {
   place_fields.draw();
}
