#include <stdio.h>
#include <stdlib.h>
#include "defs.hpp"
#include "../include/glm/glm.hpp"
#include <vector>
#include "kmeans.hpp"
#include "hmm.hpp"
#include "process.hpp"
#include "rat.hpp"

Rat *rat;
Path *path;
//KMeans *kmeans;
PlaceField *pf;
Process *process;

const char * spikes_filename;
const char * output_filename;
const char * run_filename;
int fade;

void display(void) {

	glClear(GL_COLOR_BUFFER_BIT);

	rat->draw();

	pf->drawBoxes();

//	kmeans->drawCentroids();

	glFlush();
}

void init(const char * runfilename, const char * spikefilename, bool fade) {
	glClearColor(0.0f, 0.0f, 0.2f, 0.0f);

	path = new Path(runfilename);

	rat = new Rat(glm::vec2(0.5,0.5), glm::vec2(0.1,0.1), fade ? 0.9995f : 1.0f);
	rat->addPlaceCell(new PlaceCell(spikefilename, glm::vec4(1.0f, 1.0f, 0.0f, 1.0f), true, path->getStartTime(), path->getEndTime(), output_filename));
	//rat->addPlaceCell(new PlaceCell("bon/bon_4/bon_4_2_run/spikes/spike_13_4.txt", glm::vec4(0.0f, 1.0f, 0.0f, 1.0f), true, path->getStartTime(), path->getEndTime(), "pc2.txt"));
	//rat->addPlaceCell(new PlaceCell("bon/bon_4/bon_4_2_run/spikes/spike_12_3.txt", glm::vec4(1.0f, 0.0f, 0.0f, 1.0f), true, path->getStartTime(), path->getEndTime(), "pc3.txt"));
	//rat->addPlaceCell(new PlaceCell("bon/bon_4/bon_4_2_run/spikes/spike_2_4.txt", glm::vec4(0.0f, 0.0f, 1.0f, 1.0f), true, path->getStartTime(), path->getEndTime(), "pc4.txt"));
	//rat->addPlaceCell(new PlaceCell("bon/bon_4/bon_4_2_run/spikes/spike_14_1.txt", glm::vec4(1.0f, 0.0f, 1.0f, 1.0f), true, path->getStartTime(), path->getEndTime(), "pc5.txt"));

	rat->setAndFollowPath(path);

	Path p = Path(runfilename);
	PlaceCell pc = PlaceCell(spikefilename, glm::vec4(1.0f, 1.0f, 0.0f, 1.0f), true, path->getStartTime(), path->getEndTime(), output_filename);
	//kmeans = new KMeans(1);
	//kmeans->calculateCentroids(p, pc);

	pf = new PlaceField();
	pf->findMaxDivision(p,pc);

}

void update() {
	rat->update(1);
	glutPostRedisplay();
}

void shutdown() {
	delete rat;
	delete path;
	//delete kmeans;
	delete pf;
}

void animateRats(int argc, char** argv) {
	run_filename = argv[1];
	spikes_filename = argv[2];
	output_filename = argv[3];
	fade = atoi(argv[4]);

	glutInit(&argc, argv);
	glutInitDisplayMode(GLUT_SINGLE | GLUT_RGB);
	glutInitWindowSize(500, 500);
	glutInitWindowPosition(0, 0);
	glutCreateWindow("Rats");
	glutDisplayFunc(display);
	glutIdleFunc(update);
	init(run_filename, spikes_filename, fade > 0);
	glutMainLoop();
	shutdown();
}

void processDraw(void) {
	//glClear(GL_COLOR_BUFFER_BIT);

	//glFlush();
}

void processInit() {

}

void processAnimate(int argc, char** argv) {
	glutInit(&argc, argv);
	glutInitDisplayMode(GLUT_SINGLE | GLUT_RGB);
	glutInitWindowSize(500, 500);
	glutInitWindowPosition(0, 0);
	glutCreateWindow("Rats");
	glutDisplayFunc(processDraw);

}

int main(int argc, char** argv) {

	//animateRats(argc, argv);

  processInit();
  processAnimate(argc, argv);

	process = new Process();
	process->processInput(argc, argv);

  glutMainLoop();

  delete process;

	return 0;
}
