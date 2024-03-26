

(define (problem BW-rand-5)
(:domain blocksworld-4ops)
(:objects a b c d e )
(:init
(handempty)
(ontable a)
(on b a)
(on c e)
(ontable d)
(ontable e)
(clear b)
(clear c)
(clear d)
)
(:goal
(and
(on a d)
(on c a)
(on e c))
)
)


