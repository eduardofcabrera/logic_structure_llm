

(define (problem BW-rand-5)
(:domain blocksworld-4ops)
(:objects a b c d e )
(:init
(handempty)
(on a c)
(on b d)
(ontable c)
(ontable d)
(on e b)
(clear a)
(clear e)
)
(:goal
(and
(on a d)
(on c a)
(on d e)
(on e b))
)
)


