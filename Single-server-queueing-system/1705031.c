#include <stdio.h>
#include <math.h>
#include "lcgrand.h"
#define Q_LIMIT 100
#define BUSY 1
#define IDLE 0

int next_event_type, total_custs_delayed, total_events,
    num_custs_in_queue, server_status;

float area_num_in_q, area_server_status, mean_interarrival, mean_service,
      simulation_clock, time_arrival[Q_LIMIT + 1], time_last_event, time_next_event[3],
      total_of_delays;

FILE *in, *out;

float expon(float mean)
{
    return -mean * log(lcgrand(1));
}

void timing(void)
{
    int i;
    float min_time_next_event = 1.0e+29;
    next_event_type = 0;

    for (i = 1; i <= total_events; ++i)
        if (time_next_event[i] < min_time_next_event)
        {
            min_time_next_event = time_next_event[i];
            next_event_type = i;
        }


    if (next_event_type == 0)
    {
        fprintf(out, "\nEvent list empty at time %f", simulation_clock);
        exit(1);
    }


    simulation_clock = min_time_next_event;
}



void arrive(void)
{
    float delay;

    time_next_event[1] = simulation_clock + expon(mean_interarrival);

    if (server_status == BUSY)
    {

        ++num_custs_in_queue;

        if (num_custs_in_queue > Q_LIMIT)
        {
            fprintf(out, "\nOverflow of the array time_arrival at");
            fprintf(out, " time %f", simulation_clock);
            exit(2);
        }
        time_arrival[num_custs_in_queue] = simulation_clock;
    }
    else
    {
        /// as there will be no delay
        total_of_delays += 0.0;
        ++total_custs_delayed;
        server_status = BUSY;
        time_next_event[2] = simulation_clock + expon(mean_service);
    }
}

void depart(void)
{
    int i;
    float delay;

    if (num_custs_in_queue == 0)
    {
        server_status = IDLE;
        time_next_event[2] = 1.0e+30;
    }
    else
    {
        --num_custs_in_queue;
        delay = simulation_clock - time_arrival[1];
        total_of_delays += delay;
        ++total_custs_delayed;
        time_next_event[2] = simulation_clock + expon(mean_service);
        for (i = 1; i <= num_custs_in_queue; ++i)
            time_arrival[i] = time_arrival[i + 1];
    }
}


void find_average_value(void)
{
    float time_since_last_event;
    time_since_last_event = simulation_clock - time_last_event;
    time_last_event = simulation_clock;

    area_num_in_q += num_custs_in_queue * time_since_last_event;
    area_server_status += server_status * time_since_last_event;
}


void initialize(void)
{
    simulation_clock = 0.0;
    server_status = IDLE;
    num_custs_in_queue = 0;
    time_last_event = 0.0;

    total_custs_delayed = 0;
    total_of_delays = 0.0;
    area_num_in_q = 0.0;
    area_server_status = 0.0;


    time_next_event[1] = simulation_clock + expon(mean_interarrival);
    time_next_event[2] = 1.0e+30;
}



void main()
{
    int number_of_customers;
    in = fopen("in.txt", "r");
    out = fopen("out.txt", "w");
    total_events = 2;
    fscanf(in, "%f %f %d", &mean_interarrival, &mean_service,
           &number_of_customers);

    fclose(in);

    /// writing to output file

    fprintf(out, "Single-server queueing system\n\n");
    fprintf(out, "Mean interarrival time%11.3f minutes\n\n",
            mean_interarrival);
    fprintf(out, "Mean service time%16.3f minutes\n\n", mean_service);
    fprintf(out, "Number of customers%14d\n\n", number_of_customers);

    /// initialize value for first customer
    initialize();


    while (total_custs_delayed < number_of_customers)
    {

        timing();

        find_average_value();

        switch (next_event_type)
        {
        case 1:
            arrive();
            break;
        case 2:
            depart();
            break;
        }
    }


    /// generate the report printing the required information

    fprintf(out, "\n\nAverage delay in queue%11.3f minutes\n\n",
            total_of_delays / total_custs_delayed);
    fprintf(out, "Average number in queue%10.3f\n\n",
            area_num_in_q / simulation_clock);
    fprintf(out, "Server utilization%15.3f\n\n",
            area_server_status / simulation_clock);
    fprintf(out, "Time simulation ended%12.3f minutes", simulation_clock);


    fclose(out);
    return 0;
}










