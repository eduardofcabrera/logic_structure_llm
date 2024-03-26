

(define (problem BW-rand-5)
(:domain blocksworld-4ops)
(:objects a b c d e )
(:init
(handempty)
(on a c)
(on b d)
(ontable c)
(ontable d)
(on e a)
(clear b)
(clear e)
)
(:goal
(and
(on a d)
(on c e)
(on d b))
)
)


