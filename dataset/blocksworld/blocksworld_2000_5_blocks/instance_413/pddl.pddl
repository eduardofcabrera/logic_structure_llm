

(define (problem BW-rand-5)
(:domain blocksworld-4ops)
(:objects a b c d e )
(:init
(handempty)
(on a e)
(on b d)
(ontable c)
(ontable d)
(on e c)
(clear a)
(clear b)
)
(:goal
(and
(on c d))
)
)


