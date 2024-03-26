

(define (problem BW-rand-5)
(:domain blocksworld-4ops)
(:objects a b c d e )
(:init
(handempty)
(on a b)
(on b d)
(ontable c)
(ontable d)
(on e c)
(clear a)
(clear e)
)
(:goal
(and
(on a d)
(on b c)
(on c e)
(on d b))
)
)


