from manimlib import *
import numpy as np

A0 = 5
k = 0.5
n = 1

conversiony = 191 / 255
conversionx = 63.5 / 52

slope_width = 3
sim_width = 5

def n_1_exact(x):
    if n == 1:
        return A0*np.exp(-k*x)
    if n == 2:
        return -1/(k*c + A0)

def rate_fn(y):
    return k*(y**n)

class euler_anim(Scene):
    def construct(self):
        axes = Axes((0, 10), (0, 8))
        axes.add_coordinate_labels()
        xlabel = axes.get_x_axis_label(label_tex='time (s)').set_color(WHITE)
        ylabel = axes.get_y_axis_label(label_tex='[A]').set_color(RED)
        self.add(xlabel, ylabel)
        self.play(Write(axes, lag_ratio=0.01, run_time=1))
        exact = axes.get_graph(
            lambda x: n_1_exact(x)
        )
        exact_label = axes.get_graph_label(exact, "``Experiment\"")
        self.play(
            ShowCreation(exact,
                         run_time=1),
            FadeIn(exact_label, RIGHT)
        )
        rate = Tex("Rate", "= k[", "A", "]^n").set_color(WHITE).shift(UP)
        rate[0].set_color(BLUE)
        rate[2].set_color(RED)
        self.play(FadeIn(rate))

        dot = Dot(color=RED)
        dot.move_to(axes.i2gp(0, exact))
        self.play(FadeIn(dot, scale=0.5))

        x_tracker = ValueTracker(0)
        f_always(
            dot.move_to,
            lambda: axes.i2gp(x_tracker.get_value(), exact)
        )

        rate2 = VGroup(
            DecimalNumber(
                0,
                num_decimal_places=2
            ),
            Tex("=" + str(k) + "["),
            DecimalNumber(
                0,
                num_decimal_places=2,
            ),
            Tex("]^" + str(n))
        ).arrange(RIGHT)
        rate2.move_to(rate)
        rate2.shift(DOWN)

        rate2.add_updater(
            lambda r: r[2].set_value(n_1_exact(x_tracker.get_value()))
        )
        rate2[2].set_color(RED)
        rate2.add_updater(
            lambda r: r[0].set_value(rate_fn(n_1_exact(x_tracker.get_value())))
        )
        rate2[0].set_color(BLUE)
        self.play(FadeIn(rate2))

        slope = Line().set_color(BLUE).set_stroke(width = slope_width)
        slope.add_updater(
            lambda s: s.set_points_by_ends(
                start=dot.get_center() +
                      conversionx*LEFT *
                        np.cos(
                            np.arctan(
                                rate_fn(
                                    n_1_exact(
                                        x_tracker.get_value()
                                    )
                                )
                            )
                        ) +
                      conversiony*UP *
                        np.sin(
                            np.arctan(
                                rate_fn(
                                    n_1_exact(
                                        x_tracker.get_value()
                                  )
                              )
                          )
                      ),
                end=dot.get_center() +
                      conversionx*RIGHT *
                      np.cos(
                          np.arctan(
                              rate_fn(
                                  n_1_exact(
                                      x_tracker.get_value()
                                  )
                              )
                          )
                      ) +
                      conversiony*DOWN *
                      np.sin(
                          np.arctan(
                              rate_fn(
                                  n_1_exact(
                                      x_tracker.get_value()
                                  )
                              )
                          )
                      )
            )
        )
        self.play(FadeIn(slope))
        self.play(x_tracker.animate.set_value(2), run_time=2)
        self.play(x_tracker.animate.set_value(4), run_time=2)
        self.play(x_tracker.animate.set_value(6), run_time=2)
        self.play(x_tracker.animate.set_value(0), run_time=1)


        sim_label = Tex('Simulation').set_color(GREEN).move_to(exact_label)
        self.play(FadeOut(exact),
                  FadeOut(exact_label),
                  FadeIn(sim_label))

        dt = 1
        sim_xs_dt_1 = np.arange(9, dtype=float)
        sim_ys_dt_1 = np.empty_like(sim_xs_dt_1)
        sim_ys_dt_1[0] = A0
        for i in np.arange(8):
            sim_ys_dt_1[i+1] = sim_ys_dt_1[i] - dt*rate_fn(sim_ys_dt_1[i])

        x_tracker2 = ValueTracker(0).set_value(sim_xs_dt_1[0])
        y_tracker2 = ValueTracker(0).set_value(sim_ys_dt_1[0])
        dot2 = Dot(color=RED)
        dot2.add_updater(
            lambda d: d.move_to(
                axes.get_origin() + RIGHT * x_tracker2.get_value()*conversionx + UP * y_tracker2.get_value()*conversiony
            )
        )

        x_trackersec1 = ValueTracker(0).set_value(sim_xs_dt_1[0])
        y_trackersec1 = ValueTracker(0).set_value(sim_ys_dt_1[0])


        rate3 = VGroup(
            DecimalNumber(
                0,
                num_decimal_places=2
            ),
            Tex("=" + str(k) + "["),
            DecimalNumber(
                0,
                num_decimal_places=2,
            ),
            Tex("]^" + str(n))
        ).arrange(RIGHT)
        rate3.move_to(rate2)
        rate3.add_updater(
            lambda r: r[2].set_value(y_tracker2.get_value())
        )
        rate3[2].set_color(RED)
        rate3.add_updater(
            lambda r: r[0].set_value(rate_fn(y_tracker2.get_value()))
        )
        rate3[0].set_color(BLUE)
        self.play(FadeIn(rate3),
                  FadeOut(rate2),
                  run_time = 0)



        slope2 = Line().set_color(BLUE).set_stroke(width = slope_width)
        slope2.add_updater(
            lambda s: s.set_points_by_ends(
                start=dot2.get_center() +
                      conversionx*LEFT *
                        np.cos(
                            np.arctan(
                                rate_fn(
                                    y_tracker2.get_value()
                                )
                            )
                        ) +
                      conversiony*UP *
                        np.sin(
                            np.arctan(
                                rate_fn(
                                    y_tracker2.get_value()
                              )
                          )
                      ),
                end=dot2.get_center() +
                      conversionx*RIGHT *
                      np.cos(
                          np.arctan(
                              rate_fn(
                                  y_tracker2.get_value()
                              )
                          )
                      ) +
                      conversiony*DOWN *
                      np.sin(
                          np.arctan(
                              rate_fn(
                                  y_tracker2.get_value()
                              )
                          )
                      ),
            )
        )

############## SEC 1 ################ ############## SEC 1 ################ ############## SEC 1 ################
        rts1 = 1
        sim_sec1 = Line().set_color(GREEN).set_stroke(width=sim_width).add_updater(
            lambda s: s.set_points_by_ends(
                start= axes.get_origin() + UP*sim_ys_dt_1[0]*conversiony + RIGHT*sim_xs_dt_1[0]*conversionx,
                end = axes.get_origin() + UP*y_trackersec1.get_value()*conversiony + RIGHT*x_trackersec1.get_value()*conversionx
            )
        )
        self.play(FadeIn(sim_sec1),
                  FadeOut(dot),
                  FadeIn(dot2),
                  FadeOut(slope),
                  FadeIn(slope2),
                  run_time = 0)
        self.play(
            x_trackersec1.animate.set_value(sim_xs_dt_1[1]),
            y_trackersec1.animate.set_value(sim_ys_dt_1[1]),
            run_time = rts1
        )
        self.play(
            x_tracker2.animate.set_value(sim_xs_dt_1[1]),
            y_tracker2.animate.set_value(sim_ys_dt_1[1]),
            run_time=rts1
        )

############## SEC 2 ################ ############## SEC 2 ################ ############## SEC 2 ################
        rts2 = 1
        x_trackersec2 = ValueTracker(0).set_value(sim_xs_dt_1[1])
        y_trackersec2 = ValueTracker(0).set_value(sim_ys_dt_1[1])
        sim_sec2 = Line().set_color(GREEN).set_stroke(width=sim_width).add_updater(
            lambda s: s.set_points_by_ends(
                start=axes.get_origin() + UP * sim_ys_dt_1[1] * conversiony + RIGHT * sim_xs_dt_1[1] * conversionx,
                end=axes.get_origin() + UP * y_trackersec2.get_value() * conversiony + RIGHT * x_trackersec2.get_value() * conversionx
            )
        )
        self.play(FadeIn(sim_sec2), run_time = 0)
        self.play(
            x_trackersec2.animate.set_value(sim_xs_dt_1[2]),
            y_trackersec2.animate.set_value(sim_ys_dt_1[2]),
            run_time = rts2
        )
        self.play(
            x_tracker2.animate.set_value(sim_xs_dt_1[2]),
            y_tracker2.animate.set_value(sim_ys_dt_1[2]),
            run_time=rts2
        )

############## SEC 3 ################ ############## SEC 3 ################ ############## SEC 3 ################
        rts3 = 0.5
        x_trackersec3 = ValueTracker(0).set_value(sim_xs_dt_1[2])
        y_trackersec3 = ValueTracker(0).set_value(sim_ys_dt_1[2])
        sim_sec3 = Line().set_color(GREEN).set_stroke(width=sim_width).add_updater(
            lambda s: s.set_points_by_ends(
                start=axes.get_origin() + UP * sim_ys_dt_1[2] * conversiony + RIGHT * sim_xs_dt_1[2] * conversionx,
                end=axes.get_origin() + UP * y_trackersec3.get_value() * conversiony + RIGHT * x_trackersec3.get_value() * conversionx
            )
        )
        self.play(FadeIn(sim_sec3), run_time = 0)
        self.play(
            x_trackersec3.animate.set_value(sim_xs_dt_1[3]),
            y_trackersec3.animate.set_value(sim_ys_dt_1[3]),
            run_time = rts3
        )
        self.play(
            x_tracker2.animate.set_value(sim_xs_dt_1[3]),
            y_tracker2.animate.set_value(sim_ys_dt_1[3]),
            run_time=rts3
        )

############## SEC 4 ################ ############## SEC 4 ################ ############## SEC 4 ################
        x_trackersec4 = ValueTracker(0).set_value(sim_xs_dt_1[3])
        y_trackersec4 = ValueTracker(0).set_value(sim_ys_dt_1[3])
        sim_sec4 = Line().set_color(GREEN).set_stroke(width=sim_width).add_updater(
            lambda s: s.set_points_by_ends(
                start=axes.get_origin() + UP * sim_ys_dt_1[3] * conversiony + RIGHT * sim_xs_dt_1[3] * conversionx,
                end=axes.get_origin() + UP * y_trackersec4.get_value() * conversiony + RIGHT * x_trackersec4.get_value() * conversionx
            )
        )
        self.play(FadeIn(sim_sec4), run_time = 0)
        self.play(
            x_trackersec4.animate.set_value(sim_xs_dt_1[4]),
            y_trackersec4.animate.set_value(sim_ys_dt_1[4]),
            run_time=rts3
        )
        self.play(
            x_tracker2.animate.set_value(sim_xs_dt_1[4]),
            y_tracker2.animate.set_value(sim_ys_dt_1[4]),
            run_time=rts3
        )

############## SEC 5 ################ ############## SEC 5 ################ ############## SEC 5 ################
        x_trackersec5 = ValueTracker(0).set_value(sim_xs_dt_1[4])
        y_trackersec5 = ValueTracker(0).set_value(sim_ys_dt_1[4])
        sim_sec5 = Line().set_color(GREEN).set_stroke(width=sim_width).add_updater(
            lambda s: s.set_points_by_ends(
                start=axes.get_origin() + UP * sim_ys_dt_1[4] * conversiony + RIGHT * sim_xs_dt_1[4] * conversionx,
                end=axes.get_origin() + UP * y_trackersec5.get_value() * conversiony + RIGHT * x_trackersec5.get_value() * conversionx
            )
        )
        self.play(FadeIn(sim_sec5), run_time = 0)
        self.play(
            x_trackersec5.animate.set_value(sim_xs_dt_1[5]),
            y_trackersec5.animate.set_value(sim_ys_dt_1[5]),
            run_time=rts3
        )
        self.play(
            x_tracker2.animate.set_value(sim_xs_dt_1[5]),
            y_tracker2.animate.set_value(sim_ys_dt_1[5]),
            run_time=rts3
        )


############## SEC 6 ################ ############## SEC 6 ################ ############## SEC 6 ################
        x_trackersec6 = ValueTracker(0).set_value(sim_xs_dt_1[5])
        y_trackersec6 = ValueTracker(0).set_value(sim_ys_dt_1[5])
        sim_sec6 = Line().set_color(GREEN).set_stroke(width=sim_width).add_updater(
            lambda s: s.set_points_by_ends(
                start=axes.get_origin() + UP * sim_ys_dt_1[5] * conversiony + RIGHT * sim_xs_dt_1[5] * conversionx,
                end=axes.get_origin() + UP * y_trackersec6.get_value() * conversiony + RIGHT * x_trackersec6.get_value() * conversionx
            )
        )
        self.play(FadeIn(sim_sec6), run_time = 0)
        self.play(
            x_trackersec6.animate.set_value(sim_xs_dt_1[6]),
            y_trackersec6.animate.set_value(sim_ys_dt_1[6]),
            run_time=rts3
        )
        self.play(
            x_tracker2.animate.set_value(sim_xs_dt_1[6]),
            y_tracker2.animate.set_value(sim_ys_dt_1[6]),
            run_time=rts3
        )
        self.play(
            sim_label.animate.move_to(axes.get_origin() + 0.5*UP + 1.5*RIGHT),
            FadeIn(exact_label),
            FadeIn(exact),
            FadeOut(slope2),
            FadeOut(dot2),
            FadeOut(rate3)
        )

        self.play(
            exact_label.animate.shift(RIGHT*0.01),
            run_time = 2
        )

# class euler_anim2(Scene):
#     def construct(self):
#         axes = Axes((0, 10), (0, 8))
#         axes.add_coordinate_labels()
#         xlabel = axes.get_x_axis_label(label_tex='time (s)').set_color(WHITE)
#         ylabel = axes.get_y_axis_label(label_tex='[A]').set_color(RED)
#         self.add(xlabel, ylabel)
#         self.play(Write(axes, lag_ratio=0.01, run_time=1))
#         exact = axes.get_graph(
#             lambda x: n_1_exact(x)
#         )
#         exact_label = axes.get_graph_label(exact, "Experiment")
#         self.play(
#             ShowCreation(exact,
#                          run_time=1),
#             FadeIn(exact_label, RIGHT)
#         )
#
#
#
#         rate = Tex("Rate", "= k[", "A", "]^n").set_color(WHITE).shift(UP)
#         rate[0].set_color(BLUE)
#         rate[2].set_color(RED)
#         #self.play(FadeIn(rate))
#
#         dot = Dot(color=RED)
#         dot.move_to(axes.i2gp(0, exact))
#         self.play(FadeIn(dot, scale=0.5))
#
#         x_tracker = ValueTracker(0)
#         f_always(
#             dot.move_to,
#             lambda: axes.i2gp(x_tracker.get_value(), exact)
#         )
#
#         coords = VGroup(
#             Text("x = "),
#             DecimalNumber(0),
#             Text("y = "),
#             DecimalNumber(0),
#             Text("dy/dx ="),
#             DecimalNumber(0)
#         ).add_updater(
#             lambda c: c[1].set_value(x_tracker.get_value())
#         ).add_updater(
#             lambda c: c[3].set_value(n_1_exact(x_tracker.get_value()))
#         ).add_updater(
#             lambda c: c[5].set_value(rate_fn(n_1_exact(x_tracker.get_value())))
#         ).arrange(RIGHT)
#
#         self.play(
#             FadeIn(coords)
#         )
#
#         self.play(x_tracker.animate.set_value(4), run_time=2)
#

