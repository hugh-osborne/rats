#include "kmeans.hpp"

KMeans::KMeans(int centroid_number) {
	for (int i = 0; i < centroid_number; i++) {
		centroids.push_back(glm::vec2(0.0f, 0.0f));
	}
}

void KMeans::calculateCentroids(Path *path, PlaceCell* place_cell) {
	PathPoint *pp = path->getNextPoint();
	place_cell->getNextTime();

	while (pp) {
		if (place_cell->checkNextTime() && place_cell->getCurrentTime() && (pp->time > *(place_cell->getCurrentTime()))) {
			points.push_back(pp->position);
			place_cell->getNextTime();
		}

		pp = path->getNextPoint();
	}

	int iterations = 0;
	int max_iterations = 50;

	while (!isFinished || iterations > max_iterations) {
		recalculate();
		iterations++;
	}

	for (int i = 0; i < centroids.size(); i++) {
		printf("Centroid %i : [%f,%f]\n", i, centroids[i].x, centroids[i].y);
		sprites.push_back(new Sprite("blotch.bmp", centroids[i], glm::vec2(0.05f, 0.05f), glm::vec4(1.0f,1.0f,1.0f,1.0f), 1.0f));
	}
}

void KMeans::recalculate() {

	std::vector<std::vector<glm::vec2> > centroid_points;

	for (int i = 0; i < centroids.size(); i++) {
		centroid_points.push_back(std::vector<glm::vec2>());
		centroid_points[i].push_back(points[i]);
	}

	for (int i = centroids.size(); i < points.size(); i++) {

		GLfloat dist = glm::length(centroids[0] - points[i]);
		int max_index = 0;

		for (int j = 1; j < centroids.size(); j++) {
			if (glm::length(centroids[j] - points[i]) < dist) {
				dist = glm::length(centroids[j] - points[i]);
				max_index = j;
			}
		}

		centroid_points[max_index].push_back(points[i]);
	}

	isFinished = true;

	for (int i = 0; i < centroids.size(); i++) {
		glm::vec2 avg = glm::vec2(0.0f,0.0f);
		for (int j = 0; j < centroid_points[i].size(); j++) {
			avg += centroid_points[i][j];
		}
		avg /= (GLfloat)centroid_points[i].size();
		isFinished &= avg.x == centroids[i].x && avg.y == centroids[i].y;
		centroids[i] = avg;
	}
}

void KMeans::drawCentroids() {
	for (int i = 0; i < sprites.size(); i++) {
		sprites[i]->bindTextureAndDrawTriangles();
	}
}
