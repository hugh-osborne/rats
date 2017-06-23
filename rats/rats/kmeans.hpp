#pragma once
#include <vector>
#include "defs.hpp"
#include "../include/glm/glm.hpp"
#include "path.hpp"
#include "placecell.hpp"
#include "sprite.hpp"

class KMeans {
private:
	std::vector<glm::vec2> points;
	std::vector<glm::vec2> centroids;
	std::vector<Sprite*> sprites;

	bool isFinished = false;
	void recalculate();

public:
	KMeans(int centroid_number);

	void calculateCentroids(Path *path, PlaceCell* place_cell);
	GLfloat getHighestLikelihood(glm::vec2 point);
	void drawCentroids();

};
