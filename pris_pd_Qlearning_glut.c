#include <stdio.h>
#include <stdlib.h>
#include <math.h>

#include <mc.h>

#include "glut_view_pd_best.h"

#include <time.h>
#include <gsl/gsl_rng.h>
#include <gsl/gsl_randist.h>


/***************************************************************************
 *                          Constant Declarations                           *
 ***************************************************************************/
const int NUM_CONF       = 20;
#define   LSIZE           100 //200           /*lattice size*/
#define   LL              (LSIZE*LSIZE)   	/*number of sites*/

const int INITIALSTATE   = 4;               		  /*1:random 2:one D 3:D-block 4: exact 5
													5: 2C's */
const double PROB_C	     = 0.50;//(0.3333) //0.4999895//(1.0/3.0)                 /*initial fraction of cooperators*/
const double PROB_D      = 1.0 - PROB_C; //PROB_C       		  	  /*initial fraction of defectors*/

const int    TOTALSTEPS  = 100000; //100000				      /*total number of generations (MCS)*/

#define MEASURES   1000
#define	NUM_NEIGH  4

#define FRANDOM1   (gsl_rng_uniform(r))

//#define USEGFX
//#define SELF_INTERACTION
//#define DIFFUSE

const int  C              =  1;
const int  D              = -1; //#define D (-1)
const int  MOVE			  =  0;
const int  COMPARE        =  2;

#define NUM_STATES  	   2

const int Dindex  		 = 0;
const int Cindex  		 = 1;

const int COMPAREindex   = 0;
const int MOVEindex      = 1;

const int STATES[NUM_STATES]   = {D, C};

#define NUM_ACTIONS 	   2
const int ACTIONS[NUM_ACTIONS] = {COMPARE, MOVE};

const int STATE_INDEX[NUM_STATES] = {Dindex, Cindex};

double P_DIFFUSION;
double K_FERMI;

/****** Q-Learning **********/
double        EPSILON	  = 0.02; //1.0;
const double  EPSILON_MIN = 0.15; //0.1;
//const double  EPS         = 1e-5;
const double  LAMBDA      = 0.02;
const double  ALPHA       = 0.8; //0.75;
const double  GAMMA       = 0.75; //0.75;

/***************************************************************************
*                      Variable Declarations                               *
***************************************************************************/
const int L2   = LSIZE * LSIZE;

unsigned long  right[LL], left[LL], top[LL], down[LL], neigh[LL][NUM_NEIGH];
unsigned long  num_empty_sites, empty_matrix[LL], which_empty[LL];
int            s[LL];
float 		   payoff[LL];

double		   Q[LL][NUM_STATES][NUM_ACTIONS];

unsigned long  seed, numsteps, num_c, num_cd, num_dc, num_d;
long           t[MEASURES];
double         num_c_ave[MEASURES], num_d_ave[MEASURES], num_cd_ave[MEASURES], Q_ave[MEASURES][NUM_STATES][NUM_ACTIONS];
float          TEMPTATION;

const float    SUCKER = 0.0;
const float    PP     = 0.0;
const float	   RR     = 1.0;

unsigned long  NUM_DEFECTS;

FILE           *freq,*fconf;

unsigned long int rseed;
const gsl_rng_type * T;
gsl_rng * r;

/***************************************************************************
*                           Function Declarations                          *
***************************************************************************/
void file_initialization(void);
void initialization(void);
void local_dynamics(int *s, float *payoff, unsigned long *empty_matrix,unsigned long *which_emp);
void count_neighbours(int *s, int ii, int *nc, int *nd);
void determine_neighbours(unsigned long neigh[][NUM_NEIGH]);
void initial_state(int *s, int lsize, int initialstate, double probc, double probd);

//double calculate_payoff(int ss, int nc, int nd);
double pd_payoff(int *s, int ss, int ii);
void   update_fermi(float *payoff, int *s, int *state_max, int chosen_site, float own_payoff);
//void dynamics (int *s, float *payoff,unsigned long *empty_matrix,unsigned long *which_emp);


unsigned long empty_site(unsigned long ll, int *nn,
                         unsigned long *empty_matrix, unsigned long *which_empty);
void update_empty_sites(unsigned long s1, unsigned long s2,
                        unsigned long *which_empty, unsigned long *empty_matrix);
int odd(int x);

/***************************************************************************
*                    PSEUDO-RANDOM NUMBER GENERATOR                        *
***************************************************************************/
unsigned long int set_gsl_rng(void)
{
#ifdef DEBUG
  rseed=42;
#else
  rseed=time(NULL);
#endif

  gsl_rng_env_setup();
  T = gsl_rng_default;
  r = gsl_rng_alloc (T);
  gsl_rng_set (r, rseed);

  return rseed;
}

/***************************************************************************
*                            Simulation                                    *
***************************************************************************/
extern void simulation(void)
{
	int iconf,i,j,k,l,m;
	static int ICONF=0;

	//double epsilon_test=1.0;

   while(ICONF < NUM_CONF) //FOR GLUT
   {
		for (iconf=0;iconf<NUM_CONF;++iconf)
		{
			fprintf(stdout,"Initializing conf %d\n",iconf);
			fflush(stdout);
			++ICONF;
			initialization();
			for (i=0; i<MEASURES; ++i)
			{
				while (numsteps <= t[i])
				{
					//epsilon_test = EPSILON * exp(-LAMBDA * numsteps);
					EPSILON = EPSILON_MIN;//(epsilon_test > EPSILON_MIN ? epsilon_test : EPSILON_MIN);
					//EPSILON = (epsilon_test > EPSILON_MIN ? epsilon_test : EPSILON_MIN);
					local_dynamics(s, payoff, empty_matrix, which_empty);

					++numsteps;
				}
				num_c_ave[i]  += num_c;
				num_d_ave[i]  += num_d;
				num_cd_ave[i] += num_cd+num_dc;

				for (k=num_empty_sites; k < L2; ++k)
				{
					for(l=0; l<NUM_STATES; ++l)
						for(m=0; m<NUM_ACTIONS; ++m)
							Q_ave[i][l][m] += Q[empty_matrix[k]][l][m];
				}

				if ((num_d == (L2-num_empty_sites)) || (num_c == (L2-num_empty_sites)))
				{
					for (j=i+1; j < MEASURES; ++j)
					{
						num_c_ave[j]  += num_c;
						num_d_ave[j]  += num_d;
						num_cd_ave[j] += 0.0;

						for(l=0; l<NUM_STATES; ++l)
							for(m=0; m<NUM_ACTIONS; ++m)
								Q_ave[j][l][m] = Q_ave[i][l][m];
					}
					break;
				}
			}
		}

		for(i=0;i<MEASURES;++i)
		{
			num_c_ave[i]  /= NUM_CONF;
			num_d_ave[i]  /= NUM_CONF;
			num_cd_ave[i] /= NUM_CONF;

			for(l=0; l<NUM_STATES; ++l)
				for(m=0; m<NUM_ACTIONS; ++m)
					Q_ave[i][l][m] /= NUM_CONF;

			fprintf(freq,"%ld %.6f %.6f %.6f ",t[i],num_c_ave[i],num_d_ave[i],num_cd_ave[i]);
			for(l=0; l<NUM_STATES; ++l)
				for(m=0; m<NUM_ACTIONS; ++m)
					fprintf(freq,"%.6f ", Q_ave[i][l][m]);
			fprintf(freq,"\n");
		}
		fclose(freq);

}//GLUT END!!!
  return;
}
/***************************************************************************
 *                           Determine neighbours                          *
 ***************************************************************************/
void determine_neighbours(unsigned long neigh[][(int) NUM_NEIGH])
{
	int i;

	for(i=0; i<L2; ++i)
	{
		neigh[i][0] = left[i];
		neigh[i][1] = right[i];
		neigh[i][2] = top[i];
		neigh[i][3] = down[i];
	}
	return;
}
/***************************************************************************
 *                          Random Diffusion                               *
 ***************************************************************************/
 int rand_diffusion(int *s1, int *s, unsigned long *empty_matrix,unsigned long *which_empty)
{
	int    i, j, k, s2;
	double sample_random = FRANDOM1;

	if (sample_random < P_DIFFUSION)
    {
		sample_random = FRANDOM1;
		i  = (int)((double)(NUM_NEIGH) * sample_random);  // choose random direction
		s2 = neigh[*s1][i];

		if (s[s2] == 0) // test if chosen direction is empty
		{
			s[s2] = s[*s1]; // Change strategy
			s[*s1] = 0;

			payoff[s2] = payoff[*s1]; // Change payoffs
			payoff[*s1] = 0.0;

			for(j=0; j<NUM_STATES;++j) // Change Q values
			{
				for(k=0; k<NUM_ACTIONS;++k)
				{
					Q[s2][j][k] = Q[*s1][j][k];
					Q[*s1][j][k] = 0.0;
				}
			}
			/*s1=empty_matrix[j]; neighborhood --> no-empty*/
			/*s2=j;  site --> empty*/
			update_empty_sites(*s1, s2, which_empty, empty_matrix); // emp ---> empty_matrix

			*s1 = s2; // Change position

			return 1;
		}
    }
	return 0;
}
/***************************************************************************
 *                           Local Combat                                  *
 ***************************************************************************/
void count_neighbours(int *s, int ii, int *nc, int *nd)
{
	int k;

	*nc = 0;
	*nd = 0;

#ifdef SELF_INTERACTION
	switch(s[ii])
	{
		case D: *nd = 1;
			break;
		case C: *nc = 1;
			break;
	}
#endif

   for (k=0; k<NUM_NEIGH ;++k)
	{
       switch(s[neigh[ii][k]])
		{
			case  C: ++(*nc);
				break;
			case  D: ++(*nd);
				break;
		}
    }
   return;
 }
/***************************************************************************
 *                           Payoffs                                       *
 ***************************************************************************/
/*double calculate_payoff(int SUCKER, int nc, int nd)
{
	double pay;
	switch (SUCKER)
	{
		case C: pay = RR*nc + SUCKER*nd;
				 break;
		case D: pay = TEMPTATION*nc + PP*nd;
				 break;
		default: printf("ERROR: SUCKER = %d numsteps = %ld %d %d\n",SUCKER, numsteps,nc,nd);
				 exit(1);
				 break;
	}

	return pay;
}*/

/***************************************************************************
 *                    Calculate Fermi Probability                          *
 ***************************************************************************/
double calculate_fermi_probability(int payoff_site, int payoff_neighbour){
    return 1. / (1. + exp(-(1. * payoff_neighbour - 1. * payoff_site)) / K_FERMI);
}

/***************************************************************************
 *                    Payoff comparison                                    *
 ***************************************************************************/
void update_fermi(float *payoff, int *s, int *new_state, int chosen_site, float own_payoff)
{
    int neigh_site = (int) (NUM_NEIGH * FRANDOM1);

    //printf("%f \n", calculate_fermi_probability(payoff[chosen_site], payoff[neigh[chosen_site][neigh_site]]));

    if ((s[neigh[chosen_site][neigh_site]] != 0) && (calculate_fermi_probability(payoff[chosen_site],
        payoff[neigh[chosen_site][neigh_site]]) < FRANDOM1)){
        *new_state = s[neigh[chosen_site][neigh_site]];
        return;
    }
    *new_state = s[chosen_site];

    return;
}

/***************************************************************************
 *                    Prisoner's Dilemma Payoffs                           *
 ***************************************************************************/
double pd_payoff(int *s, int ss, int ii)
{
	int nc, nd;
	double pay = 0.0;

	count_neighbours(s, ii, &nc, &nd);

	switch (ss)
	{
		case C: pay = RR * nc;// + SUCKER*nd;
				 break;
		case D: pay = TEMPTATION * nc; //+ PP * nd;
				 break;
		default: printf("ERROR: ss = %d numsteps = %ld %d %d\n", ss, numsteps, nc, nd);
				 exit(1);
				 break;
	}
	//pay = calculate_payoff(ss,nc,nd);

	return pay;
}
/***************************************************************************
 *                           Random choice                                 *
 ***************************************************************************/
void random_choice(int site, int *new_action, int *new_action_index)
{
	// Chooses an integer in [0,NUM_ACTIONS)

	*new_action_index = (int) (FRANDOM1 * NUM_ACTIONS);
	*new_action = ACTIONS[*new_action_index];

	return;
}
/***************************************************************************
 *                       Maximum Q_value per row                           *
 ***************************************************************************/
void find_maximum_Q_value(int chosen_site, int *state_index, int *maxQ_action, int *maxQ_ind, double *maxQ)
{
	int i;

	//randomly choose initial maximum value in case of ties
	random_choice(chosen_site, maxQ_action, maxQ_ind);
	*maxQ = Q[chosen_site][*state_index][*maxQ_ind];

	// now find maximum
	for (i = 0; i < NUM_ACTIONS; ++i)
		if (Q[chosen_site][*state_index][i] > *maxQ)
		{
			*maxQ     = Q[chosen_site][*state_index][i];
			*maxQ_ind = i;
		}

	//*maxQ_state = (*maxQ_ind == Cindex ? C : D);
	*maxQ_action = ACTIONS[*maxQ_ind];

	return;
}
/***************************************************************************
 *                           Local Dynamics                                *
 ***************************************************************************/
void local_dynamics (int *s, float *payoff, unsigned long *empty_matrix, unsigned long *which_emp)
{
	int stemp[L2];
	int i,j,chosen_index, chosen_site;
	int initial_s_index, new_action_index;
	int initial_s;

	double maxQ, new_maxQ;
	double reward;
	int    state_max;
	int    new_action, future_action, future_action_index;

	num_c  = 0;
	num_cd = 0;
	num_dc = 0;
	num_d  = 0;

	for (i=num_empty_sites; i < L2; ++i)
		stemp[empty_matrix[i]] = s[empty_matrix[i]];

	for (j=0; j < L2; ++j)
    {
		chosen_index = (int)(num_empty_sites + FRANDOM1*(L2-num_empty_sites));
		chosen_site  = empty_matrix[chosen_index];

		initial_s = s[chosen_site];

		if  (initial_s != 0)
		{
			initial_s_index = (initial_s == C ? Cindex : Dindex);

			//double initial_payoff  = pd_payoff(s, initial_s, chosen_site);

			if (FRANDOM1 < EPSILON) //random
				random_choice(chosen_site, &new_action, &new_action_index);
			else // greedy
				find_maximum_Q_value(chosen_site, &initial_s_index, &new_action, &new_action_index, &maxQ);

			if (new_action_index != MOVEindex)
			{
				update_fermi(payoff, s, &state_max, chosen_site, payoff[chosen_site]);

				int max_state_index = (state_max == C ? Cindex : Dindex);

				find_maximum_Q_value(chosen_site, &max_state_index, &future_action, &future_action_index, &new_maxQ);

				double final_payoff   = pd_payoff(s, initial_s, chosen_site);

				reward = final_payoff;

				s[chosen_site] = state_max;

				// Q[chosen_site][initial_s_index][new_action_index] = (1.- ALPHA)*Q[chosen_site][initial_s_index][new_action_index]  + ALPHA*(final_payoff + GAMMA*new_maxQ);
				// This is equivalent to expression above:
				Q[chosen_site][initial_s_index][new_action_index] +=  ALPHA*(reward + GAMMA*new_maxQ
										- Q[chosen_site][initial_s_index][new_action_index]);

				payoff[chosen_site] = final_payoff;

			}
			else // try to move
			{
				int moved = rand_diffusion(&chosen_site, s, empty_matrix, which_empty);
				// Chosen site possivelmente atualizado

				if (moved)
				{
    				// payoff changes in new site
    				double final_payoff  = pd_payoff(s, initial_s, chosen_site);
    				reward               = final_payoff;

                    //update_fermi(payoff, s, &state_max, chosen_site, payoff[chosen_site]);

    				find_maximum_Q_value(chosen_site, &initial_s_index, &future_action, &future_action_index, &new_maxQ);

    				Q[chosen_site][initial_s_index][new_action_index] +=  ALPHA * (reward + GAMMA * new_maxQ
    										- Q[chosen_site][initial_s_index][new_action_index] );

                    payoff[chosen_site] = reward;
				}

			}
		} // if(s1!=0)
	}
	for (i=num_empty_sites; i< L2; ++i)
	{
		int s1 = empty_matrix[i];

		switch (s[s1])
		{
			case C: {
						++num_c;
						if  (stemp[s1] == D) ++num_dc;
					 }	break;
			case D: {
						++num_d;
						if  (stemp[s1] == C) ++num_cd;

					} break;
		}
	}

#ifdef USEGFX
	view2d(LSIZE, s, numsteps, TOTALSTEPS, t, num_c, num_d, NUM_DEFECTS);
	//syst_return = system("sleep 1");
#endif

  return;
}

/***************************************************************************
*                               Main                                       *
***************************************************************************/
int main(int argc, char **argv)
{
   	if (argc != 5)
   	{
  		printf("\nThe program must be called with 4 parameters, T, NUM_DEFECTS, P_DIFFUSION and K_FERMI\n");
  		exit(1);
   	}
   	else
    {
  		TEMPTATION  = atof(argv[1]);
  		NUM_DEFECTS = atof(argv[2]);
  		P_DIFFUSION = atof(argv[3]);
        K_FERMI     = atof(argv[4]);
   	}

	seed = set_gsl_rng();	 //Start GSL Random number generator

	create_time_table_2(t, TOTALSTEPS, MEASURES);
	neighbours_2d(right, left, top, down, LSIZE);
	determine_neighbours(neigh);

	file_initialization();

#ifdef USEGFX
	char window_title[50];
	sprintf(window_title, "Prisoners Dilemma - Q learning");
	initialize_glut_display(simulation, &argc, argv, window_title);
#else
	simulation();
#endif

	//printf("Done initialize_glut_display\n"); fflush(stdout);
  return 0;
}

/***************************************************************************
 *                        File Initialization                              *
 ***************************************************************************/
void file_initialization(void)
{
	char output_file_freq[200];
	int i,j,k;

	sprintf(output_file_freq,"data/fermi/T%.2f_S_%.2f_LSIZE%d_rho%.5f_P_DIFFUSION%.2f_CONF_%d_%ld_prof.dat",
                              TEMPTATION, SUCKER, LSIZE, 1.0 - NUM_DEFECTS / ((float) LL),
                              P_DIFFUSION, NUM_CONF, seed);
	freq = fopen(output_file_freq,"w");

	fprintf(freq,"# Diffusive and Diluted Spatial Games - 2D ");//- V%s\n",VERSION);
	fprintf(freq,"# Fermi update version ");//- V%s\n",VERSION);
	fprintf(freq,"# Lattice: %d x %d = %d\n",LSIZE,LSIZE,L2);
	fprintf(freq,"# Random seed: %ld\n",seed);
	fprintf(freq,"# N_CONF = %d \n",NUM_CONF);
	fprintf(freq,"# TEMPTATION = %5.3f\n", TEMPTATION);
	fprintf(freq,"# RR = %5.3f\n", RR);
	fprintf(freq,"# SUCKER = %5.3f\n", SUCKER);

	fprintf(freq,"# rho = %.4f\n",1.0-NUM_DEFECTS/((float)L2));
	fprintf(freq,"# Num defects = %ld \n",NUM_DEFECTS);
	fprintf(freq,"# Initial prob(c) = %5.4f\n",PROB_C);
	fprintf(freq,"# Initial prob(d) = %5.4f\n",PROB_D);
	fprintf(freq,"# Prob diffusion = %5.4f\n",P_DIFFUSION);

	fprintf(freq,"# GAMMA   = %5.3f\n", GAMMA);
	fprintf(freq,"# ALPHA   = %5.3f\n", ALPHA);
	fprintf(freq,"# LAMBDA  = %5.3f\n", LAMBDA);
	fprintf(freq,"# EPSILON = %5.3f\n", EPSILON);
	fprintf(freq,"# EPSILON_MIN = %5.3f\n", EPSILON_MIN);
	fprintf(freq,"# NUM_STATES  = %d\n", NUM_STATES);
	fprintf(freq,"# NUM_ACTIONS = %d\n", NUM_ACTIONS);
	fprintf(freq,"# K_FERMI = %5.3f\n", K_FERMI);

	fprintf(freq,"# Initial configuration: ");
	switch (INITIALSTATE)
    {
		case 1 : fprintf(freq,"Random\n");
			break;
		case 2 : fprintf(freq,"One D\n");
			break;
		case 3 : fprintf(freq,"D-Block\n");
			break;
		case 4 : fprintf(freq,"Exact\n");
			break;
		case 5 : fprintf(freq,"2 C's\n");
			break;
    }
	fprintf(freq,"# Steps: Total = %5d\n",TOTALSTEPS);

	//fprintf(freq,"#t  f_c  f_d  f_ac  Qcc  Qcd Qdc Qdd P\n");

	fprintf(freq,"#t  f_c  f_d  f_ac  Qdb Qcb Qdm Qcm\n");

	for (i=0;i<MEASURES;++i)
	{
		num_c_ave[i]  = 0.0;
		num_d_ave[i]  = 0.0;
		num_cd_ave[i] = 0.0;
		for(j=0; j<NUM_STATES; ++j)
			for(k=0; k<NUM_ACTIONS; ++k)
				Q_ave[i][j][k] = 0.0;
	}

	return;
}
/***************************************************************************
 *                      Environment Initialization                         *
 ***************************************************************************/
void initialization(void)
{
	int i,j,k;

	numsteps  = 0;
	num_c     = 0;
	num_d     = 0;
	num_cd    = 0;

	initial_state(s, LSIZE, INITIALSTATE, PROB_C, PROB_D);

	num_empty_sites = empty_site(L2, s, empty_matrix, which_empty); //ja existia uma matriz which_empty

	for (i=0; i < L2; ++i)
    {
		payoff[i] = 0.0;

		switch(s[i])
		{
			case C: ++num_c;
				break;
			case D: ++num_d;
				break;
		}

		for(j = 0; j < NUM_STATES; ++j)
		{
			for(k = 0; k < NUM_ACTIONS; ++k)
				Q[i][j][k] = 0.0;//FRANDOM1;
		}
	}
	fflush(freq);

#ifdef USEGFX
	int syst_return;
	view2d(LSIZE, s, numsteps, TOTALSTEPS, t, num_c, num_d, NUM_DEFECTS);
	syst_return = system("sleep 0.5");
	if (syst_return == 1000)
		printf("Uot!\n");
#endif

  return;
}
/***********************************************************************
 *                            Initial State                             *
 ***********************************************************************/
void initial_state(int *s,  int lsize, int initialstate, double probc, double probd)

{
  int i, l2, vazios;
  double sample_random;

  l2 = lsize * lsize;
  switch (initialstate)
    {
    case 1 : for (i = 0; i < l2; ++i)
	{
	  *(s+i) = 0;
	  sample_random = FRANDOM1;
	  if (sample_random<probc) *(s+i) = 1;
	  else if (sample_random < (probc+probd)) *(s+i) = D;
	}
      break;
    case 2 : for (i = 0; i < l2; ++i)
	{
	  *(s+i) = 0;
	  sample_random = FRANDOM1;
	  if (((!odd(lsize) && i==(l2+lsize)/2))
	      || ((odd(lsize)) && (i == l2/2) ))
	    *(s+i) = D;
	  else if (sample_random<probc) *(s+i) = C;
	}
      break;
    case 3 : for (i = 0; i < l2; ++i)
	{
	  *(s+i) = 0;
	  /*if ((i==(l2+lsize)/2) || (i==(l2+lsize)/2 +1) ||
	      (i==(l2+lsize)/2 -lsize) || (i==(l2+lsize)/2 +lsize) )
	    *(s+i) = 1;
	    else *(s+i)=-1;*/
	  /*  if ((i==(l2+lsize)/2) || (i==(l2+lsize)/2 +1) ||
		(i==(l2+lsize)/2 -lsize) ||
		(i==(l2+lsize)/2-lsize+1))
	      *(s+i) = 1;
	      else *(s+i) = -1;*/
	  sample_random = FRANDOM1;
	  if ((i==(l2+lsize)/2) || (i==(l2+lsize)/2 +1) ||
	      (i==(l2+lsize)/2 -lsize) ||
	      (i==(l2+lsize)/2-lsize+1))
	    *(s+i) = -1;
	  else if (sample_random<probc) *(s+i) = 1;
	}
      break;
    case 4 : for (i = 0; i < l2; ++i)
			{
				*(s+i) = 1;
			}
      vazios=0;
      while (vazios < (int) NUM_DEFECTS)
		{
			i= (int) (FRANDOM1*l2);
			if (*(s+i)!=0)
				{
					*(s+i)=0;
					++vazios;
				}
		}
	  for (i = 0; i < l2; ++i)
		{
			if (*(s+i)!=0)
			{
				sample_random = FRANDOM1;
				if (sample_random<(probd/(probc+probd)))
				{
					*(s+i) = -1;
				}
	    }
	}
      break;
    case 5 :for (i = 0; i < l2; ++i)
			{
				*(s+i) = -1;
			}
      *(s+l2/2)=1;
      *(s+l2/2+lsize)=1;
      /**/ i=(int) (FRANDOM1*l2);
       *(s+i)=1;
       *(s+i+1)=1;
       vazios=0;
       while (vazios < (int) (l2*(1.-PROB_C-PROB_D)))
         {
           i= (int) (FRANDOM1*l2);
           if ( ( *(s+i)!=0 ) && ( *(s+i)!=1 ) )
             {
               *(s+i)=0;
               ++vazios;
             }
	    }/**/
      break;
    }
return;
}

/*********************************************************************
***                  Number and Position of Empty Sites            ***
***                      Last modified: 30/05/1999                 ***
*********************************************************************/
unsigned long empty_site(unsigned long ll, int *nn,
                         unsigned long *empty_matrix, unsigned long *which_emp)
{
	unsigned long i,k;

	k = 0;
	for (i=0; i<ll; ++i)     /* Empty sites position, starting from k==0 */
	{
		if (nn[i]==0)
		{                      /* nn represents the state */
			empty_matrix[k] = i; /* lattice number corresponding to empty site */
			which_emp[i] = k;    /* position of the empty site in the emp matrix*/
			++k;
		}
		else
		{ /* sites which are not empty are placed at the end of matrix */
			empty_matrix[ll-1-i+k] = i;
			which_emp[i]           = ll-1-i+k;
		}
    }
  return k;
}
/*********************************************************************
 ***                       Update Empty_Sites Matrix                ***
 ***                       Last modified: 24/04/1999                ***
 *********************************************************************/
void update_empty_sites(unsigned long s1, unsigned long s2,
                        unsigned long *which_empty, unsigned long *empty_matrix)
{
	unsigned long sitetmp;

	empty_matrix[which_empty[s1]] = s2;
	empty_matrix[which_empty[s2]] = s1;
	sitetmp = which_empty[s1];
	which_empty[s1] = which_empty[s2];
	which_empty[s2] = sitetmp;

	return;
}

/***************************************************************************
*                              Odd                                         *
***************************************************************************/
int odd(int x)
{
	return (x%2);
}
