

(define (problem BW-rand-5)
(:domain blocksworld-4ops)
(:objects a b c d e )
(:init
(handempty)
(on a d)
(on b e)
(ontable c)
(ontable d)
(on e c)
(clear a)
(clear b)
)
(:goal
(and
(on a b)
(on b d)
(on c e)
(on e a))
)
)


